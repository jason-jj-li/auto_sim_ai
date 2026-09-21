"""Storage layer for saving and loading simulation results."""
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import pandas as pd
from .simulation import SimulationResult


def results_to_wide(frame: pd.DataFrame) -> pd.DataFrame:
    """Return one row per persona with all features and one column per answer."""
    if frame is None or frame.empty:
        return pd.DataFrame()

    data = frame.copy()
    identity = 'persona_id' if 'persona_id' in data.columns else 'persona_name'
    population_columns = [c for c in data.columns if c.startswith('persona_')]
    preferred = [
        'persona_id', 'persona_name', 'persona_age', 'persona_gender',
        'persona_occupation', 'persona_education', 'persona_location',
    ]
    population_columns = (
        [c for c in preferred if c in population_columns]
        + sorted(c for c in population_columns if c not in preferred)
    )
    if identity not in population_columns:
        population_columns.insert(0, identity)

    population = (
        data[[identity] + [c for c in population_columns if c != identity]]
        .groupby(identity, sort=False, dropna=False)
        .first()
        .reset_index()
    )

    if 'condition' in data.columns and data['condition'].fillna('').ne('').any():
        condition = (
            data[[identity, 'condition']]
            .groupby(identity, sort=False, dropna=False)
            .first()
            .rename(columns={'condition': 'study_condition'})
            .reset_index()
        )
        population = population.merge(condition, on=identity, how='left')

    answers = data.pivot_table(
        index=identity, columns='question', values='response', aggfunc='first', sort=False,
    ).reset_index()
    answers.columns.name = None
    answers = answers.rename(columns={
        column: f"answer__{column}" for column in answers.columns if column != identity
    })
    return population.merge(answers, on=identity, how='left')


class ResultsStorage:
    """Manages saving and loading simulation results."""
    
    def __init__(self, results_dir: str = "data/results"):
        """
        Initialize results storage.
        
        Args:
            results_dir: Directory to store result files
        """
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(parents=True, exist_ok=True)
    
    def save_results(self, result: SimulationResult, base_name: Optional[str] = None) -> tuple[str, str]:
        """
        Save simulation results to both CSV and JSON.
        
        Args:
            result: SimulationResult object
            base_name: Optional base name for files (uses timestamp if None)
            
        Returns:
            Tuple of (csv_filename, json_filename)
        """
        if base_name is None:
            # Create filename from timestamp
            timestamp = datetime.fromisoformat(result.timestamp)
            base_name = f"{result.simulation_type}_{timestamp.strftime('%Y%m%d_%H%M%S_%f')}"
        
        csv_filename = f"{base_name}.csv"
        json_filename = f"{base_name}.json"
        
        # Save to CSV (flat format)
        self._save_csv(result, csv_filename)
        
        # Save to JSON (detailed format with conversation history)
        self._save_json(result, json_filename)
        
        return csv_filename, json_filename
    
    def _save_csv(self, result: SimulationResult, filename: str):
        """Save results to CSV file."""
        filepath = self.results_dir / filename

        def csv_value(value):
            """Keep scalar values readable and nested population fields lossless."""
            if isinstance(value, (list, dict, tuple)):
                return json.dumps(value, ensure_ascii=False, sort_keys=True)
            return value
        
        # Flatten data for CSV
        rows = []
        for response in result.persona_responses:
            row = {
                'timestamp': result.timestamp,
                'simulation_type': result.simulation_type,
                'persona_id': response.get('persona_id', ''),
                'persona_name': response.get('persona_name', ''),
                'persona_age': response.get('persona_age'),
                'persona_gender': response.get('persona_gender', ''),
                'persona_occupation': response.get('persona_occupation', ''),
                'question': response.get('question', ''),
                'response': response.get('response', ''),
                'condition': response.get('condition', ''),
                'wave': response.get('wave', ''),
                'wave_number': response.get('wave_number', ''),
                'validation_status': response.get('validation_status', 'not_requested'),
                'validation_error': response.get('validation_error', ''),
                'instrument': result.instrument_name or '',
            }
            # Include the complete population record. Core fields above retain
            # their stable order; additional standard/custom features are
            # appended as persona_<source column>.
            for key, value in response.items():
                if key.startswith('persona_') and key not in row:
                    row[key] = csv_value(value)
            if result.intervention_text:
                row['intervention_text'] = result.intervention_text
            rows.append(row)
        
        # Always write a CSV, including for an interrupted zero-response run,
        # so the JSON sidecar remains discoverable on the Results page.
        columns = [
            'timestamp', 'simulation_type', 'persona_id', 'persona_name',
            'persona_age', 'persona_gender', 'persona_occupation', 'question',
            'response', 'condition', 'wave', 'wave_number',
            'validation_status', 'validation_error', 'instrument'
        ]
        if result.intervention_text:
            columns.append('intervention_text')
        extra_persona_columns = sorted({
            key for row in rows for key in row
            if key.startswith('persona_') and key not in columns
        })
        columns.extend(extra_persona_columns)
        pd.DataFrame(rows, columns=columns).to_csv(filepath, index=False, encoding='utf-8')
    
    def _save_json(self, result: SimulationResult, filename: str):
        """Save results to JSON file."""
        filepath = self.results_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)

    def save_result(self, result: SimulationResult) -> tuple[str, str]:
        """Backward-compatible save using the historical timestamp basename."""
        return self.save_results(result, result.timestamp.replace(':', '-'))

    def load_result(self, timestamp: str) -> Optional[Dict[str, Any]]:
        """Backward-compatible timestamp lookup."""
        return self.load_json_result(f"{timestamp.replace(':', '-')}.json")
    
    def load_json_result(self, filename: str) -> Optional[Dict[str, Any]]:
        """
        Load a JSON result file.
        
        Args:
            filename: Name of the JSON file
            
        Returns:
            Dictionary containing result data or None if error
        """
        try:
            filepath = self.results_dir / filename
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading JSON result: {str(e)}")
            return None
    
    def load_csv_result(self, filename: str) -> Optional[pd.DataFrame]:
        """
        Load a CSV result file.
        
        Args:
            filename: Name of the CSV file
            
        Returns:
            DataFrame or None if error
        """
        try:
            filepath = self.results_dir / filename
            return pd.read_csv(filepath)
        except Exception as e:
            print(f"Error loading CSV result: {str(e)}")
            return None
    
    def list_results(self) -> List[Dict[str, Any]]:
        """
        List all result files with metadata.

        Reads each JSON sidecar for simulation_type, model, seed and counts.
        Falls back to filename parsing when the JSON is missing/corrupt —
        and strips the trailing _YYYYMMDD_HHMMSS before type extraction so
        multi-word types (message_testing, ab_testing) survive.

        Returns:
            List of dictionaries with file info
        """
        import json as _json
        import re
        results = []

        for filepath in sorted(self.results_dir.glob("*.csv"), reverse=True):
            name = filepath.stem
            file_info = {
                'csv_file': filepath.name,
                'json_file': f"{name}.json",
                'name': name,
                'modified': datetime.fromtimestamp(filepath.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                # filename fallback: strip trailing date-time stamp
                'type': re.sub(r'_\d{8}_\d{6}(?:_\d{6})?$', '', name),
            }

            json_path = self.results_dir / file_info['json_file']
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    meta = _json.load(f)
                file_info['type'] = meta.get('simulation_type', file_info['type'])
                md = meta.get('metadata') or {}
                file_info['model'] = md.get('model', '')
                file_info['seed'] = md.get('seed', '')
                file_info['n_responses'] = len(meta.get('responses', []))
                file_info['n_questions'] = len(meta.get('questions', []))
            except Exception:
                pass  # filename fallback fields already set

            results.append(file_info)

        return results
    
    def delete_result(self, base_name: str) -> bool:
        """
        Delete both CSV and JSON files for a result.
        
        Args:
            base_name: Base name of the result files (without extension)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if ':' in base_name:
                base_name = base_name.replace(':', '-')
            csv_file = self.results_dir / f"{base_name}.csv"
            json_file = self.results_dir / f"{base_name}.json"
            
            if csv_file.exists():
                csv_file.unlink()
            if json_file.exists():
                json_file.unlink()
            
            return True
        except Exception as e:
            print(f"Error deleting result: {str(e)}")
            return False
    
    def clear_all_results(self) -> tuple[int, int]:
        """
        Delete all result files (CSV and JSON).
        
        Returns:
            Tuple of (number of files deleted, number of errors)
        """
        deleted_count = 0
        error_count = 0
        
        try:
            # Delete all CSV files
            for csv_file in self.results_dir.glob("*.csv"):
                try:
                    csv_file.unlink()
                    deleted_count += 1
                except Exception as e:
                    print(f"Error deleting {csv_file.name}: {str(e)}")
                    error_count += 1
            
            # Delete all JSON files
            for json_file in self.results_dir.glob("*.json"):
                try:
                    json_file.unlink()
                    deleted_count += 1
                except Exception as e:
                    print(f"Error deleting {json_file.name}: {str(e)}")
                    error_count += 1
            
            return deleted_count, error_count
        except Exception as e:
            print(f"Error clearing results: {str(e)}")
            return deleted_count, error_count
