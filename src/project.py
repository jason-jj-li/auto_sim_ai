"""Project export and import for sharing studies."""
import json
import zipfile
import shutil
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime


class ProjectManager:
    """Manages project export and import."""
    
    def __init__(
        self,
        workspace_dir: str = ".",
        export_dir: str = "exports"
    ):
        """
        Initialize project manager.
        
        Args:
            workspace_dir: Root workspace directory
            export_dir: Directory for exported projects
        """
        self.workspace_dir = Path(workspace_dir)
        self.export_dir = Path(export_dir)
        self.export_dir.mkdir(parents=True, exist_ok=True)
    
    def export_project(
        self,
        project_name: str,
        include_personas: bool = True,
        include_survey_configs: bool = True,
        include_results: bool = False,
        description: str = ""
    ) -> str:
        """
        Export project as a zip file.
        
        Args:
            project_name: Name for the exported project
            include_personas: Whether to include personas
            include_survey_configs: Whether to include survey configurations
            include_results: Whether to include simulation results
            description: Project description
            
        Returns:
            Path to exported zip file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_name = f"{project_name}_{timestamp}"
        export_path = self.export_dir / f"{export_name}.zip"
        
        # Create temporary directory for staging
        temp_dir = self.export_dir / f"temp_{export_name}"
        temp_dir.mkdir(exist_ok=True)
        
        try:
            # Create project metadata
            metadata = {
                'project_name': project_name,
                'description': description,
                'export_date': datetime.now().isoformat(),
                'includes': {
                    'personas': include_personas,
                    'survey_configs': include_survey_configs,
                    'results': include_results
                }
            }
            
            with open(temp_dir / "project_metadata.json", 'w') as f:
                json.dump(metadata, f, indent=2)
            
            # Copy personas
            if include_personas:
                personas_src = self.workspace_dir / "data" / "personas"
                if personas_src.exists():
                    personas_dst = temp_dir / "personas"
                    shutil.copytree(personas_src, personas_dst)
            
            # Copy survey configs
            if include_survey_configs:
                configs_src = self.workspace_dir / "data" / "survey_configs"
                if configs_src.exists():
                    configs_dst = temp_dir / "survey_configs"
                    shutil.copytree(configs_src, configs_dst)
            
            # Copy results
            if include_results:
                results_src = self.workspace_dir / "data" / "results"
                if results_src.exists():
                    results_dst = temp_dir / "results"
                    shutil.copytree(results_src, results_dst)
            
            # Create zip file
            with zipfile.ZipFile(export_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in temp_dir.rglob("*"):
                    if file_path.is_file():
                        arcname = file_path.relative_to(temp_dir)
                        zipf.write(file_path, arcname)
            
            return str(export_path)
        
        finally:
            # Cleanup temp directory
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
    
    def import_project(
        self,
        zip_path: str,
        merge: bool = True,
        overwrite: bool = False
    ) -> Dict[str, Any]:
        """
        Import project from zip file.
        
        Args:
            zip_path: Path to project zip file
            merge: If True, merge with existing data; if False, replace
            overwrite: Whether to overwrite existing files with same names
            
        Returns:
            Import summary
        """
        zip_path = Path(zip_path)
        if not zip_path.exists():
            return {'error': 'Zip file not found'}
        
        # Create temporary extraction directory
        temp_dir = self.export_dir / f"temp_import_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        temp_dir.mkdir(exist_ok=True)
        
        try:
            # Extract zip
            with zipfile.ZipFile(zip_path, 'r') as zipf:
                zipf.extractall(temp_dir)
            
            # Read metadata
            metadata_path = temp_dir / "project_metadata.json"
            if metadata_path.exists():
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
            else:
                metadata = {}
            
            imported_counts = {
                'personas': 0,
                'survey_configs': 0,
                'results': 0
            }
            
            # Import personas
            personas_src = temp_dir / "personas"
            if personas_src.exists():
                personas_dst = self.workspace_dir / "data" / "personas"
                personas_dst.mkdir(parents=True, exist_ok=True)
                
                for persona_file in personas_src.glob("*.json"):
                    dst_file = personas_dst / persona_file.name
                    if not dst_file.exists() or overwrite:
                        shutil.copy(persona_file, dst_file)
                        imported_counts['personas'] += 1
            
            # Import survey configs
            configs_src = temp_dir / "survey_configs"
            if configs_src.exists():
                configs_dst = self.workspace_dir / "data" / "survey_configs"
                configs_dst.mkdir(parents=True, exist_ok=True)
                
                for config_file in configs_src.glob("*.json"):
                    dst_file = configs_dst / config_file.name
                    if not dst_file.exists() or overwrite:
                        shutil.copy(config_file, dst_file)
                        imported_counts['survey_configs'] += 1
            
            # Import results
            results_src = temp_dir / "results"
            if results_src.exists():
                results_dst = self.workspace_dir / "data" / "results"
                results_dst.mkdir(parents=True, exist_ok=True)
                
                for result_file in results_src.glob("*"):
                    if result_file.is_file():
                        dst_file = results_dst / result_file.name
                        if not dst_file.exists() or overwrite:
                            shutil.copy(result_file, dst_file)
                            imported_counts['results'] += 1
            
            return {
                'success': True,
                'project_name': metadata.get('project_name', 'Unknown'),
                'imported': imported_counts,
                'metadata': metadata
            }
        
        except Exception as e:
            return {'error': str(e)}
        
        finally:
            # Cleanup
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
    
    def list_exported_projects(self) -> List[Dict[str, Any]]:
        """
        List all exported projects.
        
        Returns:
            List of project information dictionaries
        """
        projects = []
        
        for zip_file in self.export_dir.glob("*.zip"):
            try:
                with zipfile.ZipFile(zip_file, 'r') as zipf:
                    if "project_metadata.json" in zipf.namelist():
                        with zipf.open("project_metadata.json") as f:
                            metadata = json.load(f)
                        
                        projects.append({
                            'filename': zip_file.name,
                            'path': str(zip_file),
                            'size_mb': zip_file.stat().st_size / (1024 * 1024),
                            'modified': datetime.fromtimestamp(zip_file.stat().st_mtime).isoformat(),
                            **metadata
                        })
            except Exception as e:
                print(f"Error reading {zip_file}: {e}")
                continue
        
        return sorted(projects, key=lambda x: x.get('export_date', ''), reverse=True)
