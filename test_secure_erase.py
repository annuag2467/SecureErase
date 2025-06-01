import pytest
import os
import tempfile
import shutil
from unittest.mock import Mock, patch, mock_open
from pathlib import Path

# Import the classes we want to test
from erasure.overwrite import Overwriter
from utils.logger import Logger
from cli.cli import SecureEraseCLI


class TestOverwriter:
    """Test cases for the Overwriter class"""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        # Cleanup
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def overwriter(self):
        """Create an Overwriter instance with a mock logger"""
        mock_logger = Mock(spec=Logger)
        return Overwriter(mock_logger)
    
    def test_overwrite_single_file_success(self, overwriter, temp_dir):
        """Test successful overwriting of a single file"""
        # Create a test file
        test_file = os.path.join(temp_dir, "test_file.txt")
        test_content = "This is secret content that should be erased"
        
        with open(test_file, 'w') as f:
            f.write(test_content)
        
        # Verify file exists before erasure
        assert os.path.exists(test_file)
        assert os.path.getsize(test_file) > 0
        
        # Perform secure erasure
        result = overwriter.overwrite_and_delete(test_file, passes=1)
        
        # Verify erasure was successful
        assert result is True
        assert not os.path.exists(test_file)
        overwriter.logger.log.assert_called_once()
    
    def test_overwrite_empty_file(self, overwriter, temp_dir):
        """Test handling of empty files"""
        # Create an empty test file
        test_file = os.path.join(temp_dir, "empty_file.txt")
        Path(test_file).touch()
        
        assert os.path.exists(test_file)
        assert os.path.getsize(test_file) == 0
        
        # Perform secure erasure
        result = overwriter.overwrite_and_delete(test_file, passes=3)
        
        # Verify erasure was successful
        assert result is True
        assert not os.path.exists(test_file)
        overwriter.logger.log.assert_called_once_with(test_file, 3, success=True)
    
    def test_overwrite_nonexistent_file(self, overwriter):
        """Test handling of non-existent files"""
        nonexistent_file = "/path/to/nonexistent/file.txt"
        
        result = overwriter.overwrite_and_delete(nonexistent_file, passes=3)
        
        assert result is False
        overwriter.logger.log.assert_called_once_with(nonexistent_file, 3, success=False)
    
    def test_process_directory(self, overwriter, temp_dir):
        """Test processing of a directory with multiple files"""
        # Create multiple test files
        file1 = os.path.join(temp_dir, "file1.txt")
        file2 = os.path.join(temp_dir, "file2.txt")
        
        with open(file1, 'w') as f:
            f.write("Content 1")
        with open(file2, 'w') as f:
            f.write("Content 2")
        
        # Create a subdirectory with a file
        subdir = os.path.join(temp_dir, "subdir")
        os.makedirs(subdir)
        file3 = os.path.join(subdir, "file3.txt")
        with open(file3, 'w') as f:
            f.write("Content 3")
        
        # Verify files exist
        assert os.path.exists(file1)
        assert os.path.exists(file2)
        assert os.path.exists(file3)
        
        # Process the directory
        result = overwriter.process_path(temp_dir, passes=1)
        
        # Verify all files were processed
        assert not os.path.exists(file1)
        assert not os.path.exists(file2)
        assert not os.path.exists(file3)
        # Note: directories might still exist if not completely empty
        
        # Verify logger was called for each file
        assert overwriter.logger.log.call_count == 3
    



class TestLogger:
    """Test cases for the Logger class"""
    
    @pytest.fixture
    def temp_log_file(self):
        """Create a temporary log file"""
        fd, temp_log = tempfile.mkstemp(suffix='.csv')
        os.close(fd)
        yield temp_log
        # Cleanup
        if os.path.exists(temp_log):
            os.remove(temp_log)
    
    def test_logger_initialization(self, temp_log_file):
        """Test logger initialization creates proper CSV headers"""
        # Remove the temp file so logger creates it fresh
        os.remove(temp_log_file)
        
        logger = Logger(temp_log_file)
        
        # Verify file was created with headers
        assert os.path.exists(temp_log_file)
        
        with open(temp_log_file, 'r') as f:
            first_line = f.readline().strip()
            expected_headers = "Timestamp,File Path,Passes,Success,File Size"
            assert first_line == expected_headers
    
    def test_log_successful_operation(self, temp_log_file):
        """Test logging a successful operation"""
        # Remove the temp file so logger creates it fresh
        os.remove(temp_log_file)
        
        logger = Logger(temp_log_file)
        
        test_file_path = "/test/file.txt"
        logger.log(test_file_path, passes=3, success=True, file_size=1024)
        
        # Read the log file and verify entry
        with open(temp_log_file, 'r') as f:
            lines = f.readlines()
            # Should have header + 1 log entry
            assert len(lines) == 2
            
        # Verify the logged data contains expected information
        log_entry = lines[1]
        assert test_file_path in log_entry
        assert "3" in log_entry  # passes
        assert "Yes" in log_entry  # success
        assert "1024" in log_entry  # file_size
    
    def test_get_log_summary(self, temp_log_file):
        """Test getting a summary of logged operations"""
        # Remove the temp file so logger creates it fresh
        os.remove(temp_log_file)
        
        logger = Logger(temp_log_file)
        
        # Log some operations
        logger.log("/file1.txt", 3, True)
        logger.log("/file2.txt", 1, False)
        logger.log("/file3.txt", 2, True)
        
        summary = logger.get_log_summary()
        
        assert summary["total"] == 3
        assert summary["successful"] == 2
        assert summary["failed"] == 1


class TestSecureEraseCLI:
    """Test cases for the CLI interface"""
    
    @pytest.fixture
    def cli(self):
        """Create a CLI instance"""
        return SecureEraseCLI()
    
    @patch('builtins.input')
    def test_get_paths_interactively_single_path(self, mock_input, cli):
        """Test interactive path collection with single path"""
        mock_input.return_value = "/path/to/file.txt"
        
        paths = cli.get_paths_interactively()
        
        assert paths == ["/path/to/file.txt"]
    
    @patch('builtins.input')
    def test_get_paths_interactively_multiple_paths(self, mock_input, cli):
        """Test interactive path collection with multiple paths"""
        mock_input.return_value = "/file1.txt, /file2.txt, /file3.txt"
        
        paths = cli.get_paths_interactively()
        
        assert paths == ["/file1.txt", "/file2.txt", "/file3.txt"]
    
    @patch('builtins.input')
    def test_get_paths_interactively_empty_input(self, mock_input, cli):
        """Test interactive path collection with empty input"""
        mock_input.return_value = ""
        
        paths = cli.get_paths_interactively()
        
        assert paths == []
    
    @patch('builtins.input')
    def test_get_passes_interactively_default(self, mock_input, cli):
        """Test interactive passes collection with default value"""
        mock_input.return_value = ""  # Empty input should use default
        
        passes = cli._get_passes_interactively()
        
        assert passes == 3
    
    @patch('builtins.input')
    def test_get_passes_interactively_custom_value(self, mock_input, cli):
        """Test interactive passes collection with custom value"""
        mock_input.return_value = "5"
        
        passes = cli._get_passes_interactively()
        
        assert passes == 5
    
    @patch('builtins.input')
    def test_get_passes_interactively_invalid_then_valid(self, mock_input, cli):
        """Test interactive passes collection with invalid then valid input"""
        # First invalid, then valid input
        mock_input.side_effect = ["invalid", "7"]
        
        passes = cli._get_passes_interactively()
        
        assert passes == 7
        assert mock_input.call_count == 2





# Test configuration and fixtures that apply to all tests
@pytest.fixture(autouse=True)
def setup_test_environment():
    """Setup test environment before each test"""
    # Ensure we're not accidentally affecting real files
    os.environ['PYTEST_RUNNING'] = '1'
    yield
    # Cleanup after test
    if 'PYTEST_RUNNING' in os.environ:
        del os.environ['PYTEST_RUNNING']


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])