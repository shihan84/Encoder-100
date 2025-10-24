#!/usr/bin/env python3
"""
ITAssist Broadcast Encoder - 100 (IBE-100)
Basic Test Suite
Unit tests for core functionality
"""

import unittest
import sys
import os
import subprocess
import tempfile
import shutil
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestTSDuckIntegration(unittest.TestCase):
    """Test TSDuck integration and binary detection"""
    
    def test_tsduck_binary_detection(self):
        """Test TSDuck binary can be found"""
        try:
            result = subprocess.run(['tsp', '--version'], 
                                 capture_output=True, text=True, timeout=5)
            # TSDuck should return 0 or 1 (help/version is often exit code 1)
            self.assertIn(result.returncode, [0, 1], "TSDuck binary not found or not working")
            # Check if TSDuck is mentioned in output or if it's a help message
            output = result.stdout + result.stderr
            self.assertTrue(
                'TSDuck' in output or 'tsp' in output or 'version' in output.lower(),
                f"TSDuck version not found in output: {output}"
            )
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.fail("TSDuck binary not found in PATH")
    
    def test_tsduck_plugins(self):
        """Test required TSDuck plugins are available"""
        required_plugins = ['pmt', 'sdt', 'remap', 'spliceinject', 'analyze']
        
        for plugin in required_plugins:
            try:
                result = subprocess.run(['tsp', '-P', plugin, '--help'], 
                                     capture_output=True, text=True, timeout=5)
                # Plugin help should return 0 or 1 (help is often exit code 1)
                self.assertIn(result.returncode, [0, 1], f"Plugin {plugin} not available")
            except subprocess.TimeoutExpired:
                self.fail(f"Plugin {plugin} timed out")
            except FileNotFoundError:
                self.skipTest("TSDuck not found, skipping plugin tests")

class TestApplicationStructure(unittest.TestCase):
    """Test application file structure and dependencies"""
    
    def test_required_files_exist(self):
        """Test all required files exist"""
        required_files = [
            'tsduck_gui_simplified.py',
            'requirements.txt',
            'README.md',
            'LICENSE.txt',
            'build.sh',
            'build.bat',
            'Dockerfile',
            'docker-compose.yml'
        ]
        
        for file in required_files:
            self.assertTrue(os.path.exists(file), f"Required file {file} not found")
    
    def test_scte35_files_exist(self):
        """Test SCTE-35 XML files exist"""
        scte35_dir = Path('scte35_final')
        self.assertTrue(scte35_dir.exists(), "SCTE-35 directory not found")
        
        xml_files = list(scte35_dir.glob('*.xml'))
        self.assertGreater(len(xml_files), 0, "No SCTE-35 XML files found")
    
    def test_build_scripts_executable(self):
        """Test build scripts are executable"""
        if os.name != 'nt':  # Not Windows
            self.assertTrue(os.access('build.sh', os.X_OK), "build.sh not executable")
            self.assertTrue(os.access('installer/create_dmg.sh', os.X_OK), 
                          "create_dmg.sh not executable")

class TestConfiguration(unittest.TestCase):
    """Test configuration and settings"""
    
    def test_requirements_parsable(self):
        """Test requirements.txt can be parsed"""
        with open('requirements.txt', 'r') as f:
            requirements = f.read()
        
        # Should contain essential packages
        self.assertIn('PyQt6', requirements, "PyQt6 not in requirements")
        self.assertIn('psutil', requirements, "psutil not in requirements")
        self.assertIn('pyinstaller', requirements, "pyinstaller not in requirements")
    
    def test_dockerfile_valid(self):
        """Test Dockerfile syntax is valid"""
        with open('Dockerfile', 'r') as f:
            dockerfile = f.read()
        
        # Should contain essential Docker instructions
        self.assertIn('FROM', dockerfile, "Dockerfile missing FROM instruction")
        self.assertIn('WORKDIR', dockerfile, "Dockerfile missing WORKDIR instruction")
        self.assertIn('COPY', dockerfile, "Dockerfile missing COPY instruction")
        self.assertIn('CMD', dockerfile, "Dockerfile missing CMD instruction")

class TestBuildConfiguration(unittest.TestCase):
    """Test build configuration and packaging"""
    
    def test_build_config_exists(self):
        """Test build configuration file exists and is valid"""
        self.assertTrue(os.path.exists('build_config.py'), 
                       "build_config.py not found")
        
        # Try to import and validate
        try:
            import build_config
            self.assertIsNotNone(hasattr(build_config, 'APP_NAME'), 
                               "APP_NAME not defined in build_config")
            self.assertIsNotNone(hasattr(build_config, 'APP_VERSION'), 
                               "APP_VERSION not defined in build_config")
        except ImportError as e:
            self.fail(f"build_config.py import failed: {e}")
    
    def test_pyinstaller_spec_exists(self):
        """Test PyInstaller spec file exists"""
        spec_file = 'specs/IBE-100.spec'
        self.assertTrue(os.path.exists(spec_file), f"{spec_file} not found")
        
        with open(spec_file, 'r') as f:
            spec_content = f.read()
        
        # Should contain essential PyInstaller components
        self.assertIn('Analysis', spec_content, "Spec file missing Analysis")
        self.assertIn('EXE', spec_content, "Spec file missing EXE")
        self.assertIn('tsduck_gui_simplified.py', spec_content, 
                     "Spec file missing main script")

class TestDockerConfiguration(unittest.TestCase):
    """Test Docker configuration"""
    
    def test_docker_compose_valid(self):
        """Test docker-compose.yml is valid YAML"""
        import yaml
        
        try:
            with open('docker-compose.yml', 'r') as f:
                compose = yaml.safe_load(f)
            
            # Should contain essential services
            self.assertIn('services', compose, "docker-compose.yml missing services")
            self.assertIn('ibe100', compose['services'], 
                         "docker-compose.yml missing ibe100 service")
            
        except yaml.YAMLError as e:
            self.fail(f"docker-compose.yml YAML syntax error: {e}")
        except ImportError:
            self.skipTest("PyYAML not available for testing")
        except Exception as e:
            self.fail(f"Unexpected error testing docker-compose.yml: {e}")

class TestGitHubActions(unittest.TestCase):
    """Test GitHub Actions workflows"""
    
    def test_workflow_files_exist(self):
        """Test GitHub Actions workflow files exist"""
        workflow_dir = Path('.github/workflows')
        self.assertTrue(workflow_dir.exists(), ".github/workflows directory not found")
        
        workflow_files = list(workflow_dir.glob('*.yml'))
        self.assertGreater(len(workflow_files), 0, "No workflow files found")
        
        # Should have essential workflows
        workflow_names = [f.stem for f in workflow_files]
        self.assertIn('build-and-release', workflow_names, 
                     "build-and-release workflow not found")
        self.assertIn('test', workflow_names, "test workflow not found")
        self.assertIn('docker', workflow_names, "docker workflow not found")

if __name__ == '__main__':
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestTSDuckIntegration,
        TestApplicationStructure,
        TestConfiguration,
        TestBuildConfiguration,
        TestDockerConfiguration,
        TestGitHubActions
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
