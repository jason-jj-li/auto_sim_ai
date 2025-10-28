"""Storage layer for saving and loading simulation results."""
import json
import csv
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import pandas as pd
from .simulation import SimulationResult


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
            base_name = f"{result.simulation_type}_{timestamp.strftime('%Y%m%d_%H%M%S')}"
        
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
        
        # Flatten data for CSV
        rows = []
        for response in result.persona_responses:
            row = {
                'timestamp': result.timestamp,
                'simulation_type': result.simulation_type,
                'persona_name': response['persona_name'],
                'persona_age': response['persona_age'],
                'persona_gender': response['persona_gender'],
                'persona_occupation': response['persona_occupation'],
                'question': response['question'],
                'response': response['response'],
                'instrument': result.instrument_name or ''
            }
            if result.intervention_text:
                row['intervention_text'] = result.intervention_text
            rows.append(row)
        
        # Write to CSV
        if rows:
            df = pd.DataFrame(rows)
            df.to_csv(filepath, index=False)
    
    def _save_json(self, result: SimulationResult, filename: str):
        """Save results to JSON file."""
        filepath = self.results_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(result.to_dict(), f, indent=2)
    
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
            with open(filepath, 'r') as f:
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
    
    def list_results(self) -> List[Dict[str, str]]:
        """
        List all result files with metadata.
        
        Returns:
            List of dictionaries with file info
        """
        results = []
        
        for filepath in sorted(self.results_dir.glob("*.csv"), reverse=True):
            # Try to parse info from filename
            name = filepath.stem
            parts = name.split('_')
            
            file_info = {
                'csv_file': filepath.name,
                'json_file': f"{name}.json",
                'name': name,
                'modified': datetime.fromtimestamp(filepath.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            }
            
            if len(parts) >= 1:
                file_info['type'] = parts[0]
            
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

