#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for ops.mcp_tools_instance module
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestGetInstanceInCmdb(unittest.TestCase):
    """Test cases for get_instance_in_cmdb function"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Mock the problematic imports before importing the module
        self.cmdb_mcp_server_mock = MagicMock()
        self.mcp_mock = MagicMock()
        self.cmdb_mcp_server_mock.mcp = self.mcp_mock
        
        # Mock the decorator to be a no-op
        self.mcp_mock.tool.return_value = lambda func: func
        
        # Patch the imports
        sys.modules['cmdb_mcp_server'] = self.cmdb_mcp_server_mock
        sys.modules['fastmcp'] = MagicMock()
        
        # Now we can safely import the function
        from ops.mcp_tools_instance import get_instance_in_cmdb
        self.get_instance_in_cmdb = get_instance_in_cmdb

    def tearDown(self):
        """Clean up after each test."""
        # Remove mocked modules
        if 'cmdb_mcp_server' in sys.modules:
            del sys.modules['cmdb_mcp_server']
        if 'fastmcp' in sys.modules:
            del sys.modules['fastmcp']
        if 'ops.mcp_tools_instance' in sys.modules:
            del sys.modules['ops.mcp_tools_instance']
        
    @patch('ops.mcp_tools_instance.CmdbClient')
    def test_get_instance_with_instance_id_success(self, mock_cmdb_client_class):
        """Test successful retrieval of instance by instance ID"""
        # Arrange
        mock_client_instance = Mock()
        mock_cmdb_client_class.return_value = mock_client_instance
        
        expected_response = {
            'data': {
                'list': [
                    {
                        'instance_id': 'i-1234567890abcdef0',
                        'public_ip': '203.0.113.1',
                        'private_ip': '10.0.1.100',
                        'name': 'test-instance',
                        'status': 'running'
                    }
                ]
            }
        }
        mock_client_instance.get_assets.return_value = expected_response
        
        # Act
        result = self.get_instance_in_cmdb(instance_id='i-1234567890abcdef0', public_ip='', private_ip='')
        
        # Assert
        mock_cmdb_client_class.assert_called_once()
        mock_client_instance.get_assets.assert_called_once_with(
            catalog='vm',
            filters={'instance_id': 'i-1234567890abcdef0'}
        )
        
        expected_result = {
            'provided': {'instance_id': 'i-1234567890abcdef0'},
            'match_list': expected_response['data']['list']
        }
        self.assertEqual(result, expected_result)

    @patch('ops.mcp_tools_instance.CmdbClient')
    def test_get_instance_with_public_ip_success(self, mock_cmdb_client_class):
        """Test successful retrieval of instance by public IP"""
        # Arrange
        mock_client_instance = Mock()
        mock_cmdb_client_class.return_value = mock_client_instance
        
        expected_response = {
            'data': {
                'list': [
                    {
                        'instance_id': 'i-1234567890abcdef0',
                        'public_ip': '203.0.113.1',
                        'private_ip': '10.0.1.100',
                        'name': 'test-instance',
                        'status': 'running'
                    }
                ]
            }
        }
        mock_client_instance.get_assets.return_value = expected_response
        
        # Act
        result = self.get_instance_in_cmdb(instance_id='', public_ip='203.0.113.1', private_ip='')
        
        # Assert
        mock_cmdb_client_class.assert_called_once()
        mock_client_instance.get_assets.assert_called_once_with(
            catalog='vm',
            filters={'public_ip': '203.0.113.1'}
        )
        
        expected_result = {
            'provided': {'public_ip': '203.0.113.1'},
            'match_list': expected_response['data']['list']
        }
        self.assertEqual(result, expected_result)

    @patch('ops.mcp_tools_instance.CmdbClient')
    def test_get_instance_with_private_ip_success(self, mock_cmdb_client_class):
        """Test successful retrieval of instance by private IP"""
        # Arrange
        mock_client_instance = Mock()
        mock_cmdb_client_class.return_value = mock_client_instance
        
        expected_response = {
            'data': {
                'list': [
                    {
                        'instance_id': 'i-1234567890abcdef0',
                        'public_ip': '203.0.113.1',
                        'private_ip': '10.0.1.100',
                        'name': 'test-instance',
                        'status': 'running'
                    }
                ]
            }
        }
        mock_client_instance.get_assets.return_value = expected_response
        
        # Act
        result = self.get_instance_in_cmdb(instance_id='', public_ip='', private_ip='10.0.1.100')
        
        # Assert
        mock_cmdb_client_class.assert_called_once()
        mock_client_instance.get_assets.assert_called_once_with(
            catalog='vm',
            filters={'private_ip': '10.0.1.100'}
        )
        
        expected_result = {
            'provided': {'private_ip': '10.0.1.100'},
            'match_list': expected_response['data']['list']
        }
        self.assertEqual(result, expected_result)

    @patch('ops.mcp_tools_instance.CmdbClient')
    def test_get_instance_with_all_parameters_success(self, mock_cmdb_client_class):
        """Test successful retrieval of instance with all parameters"""
        # Arrange
        mock_client_instance = Mock()
        mock_cmdb_client_class.return_value = mock_client_instance
        
        expected_response = {
            'data': {
                'list': [
                    {
                        'instance_id': 'i-1234567890abcdef0',
                        'public_ip': '203.0.113.1',
                        'private_ip': '10.0.1.100',
                        'name': 'test-instance',
                        'status': 'running'
                    }
                ]
            }
        }
        mock_client_instance.get_assets.return_value = expected_response
        
        # Act
        result = self.get_instance_in_cmdb(
            instance_id='i-1234567890abcdef0', 
            public_ip='203.0.113.1', 
            private_ip='10.0.1.100'
        )
        
        # Assert
        mock_cmdb_client_class.assert_called_once()
        mock_client_instance.get_assets.assert_called_once_with(
            catalog='vm',
            filters={
                'instance_id': 'i-1234567890abcdef0',
                'public_ip': '203.0.113.1',
                'private_ip': '10.0.1.100'
            }
        )
        
        expected_result = {
            'provided': {
                'instance_id': 'i-1234567890abcdef0',
                'public_ip': '203.0.113.1',
                'private_ip': '10.0.1.100'
            },
            'match_list': expected_response['data']['list']
        }
        self.assertEqual(result, expected_result)

    @patch('ops.mcp_tools_instance.CmdbClient')
    def test_get_instance_with_two_parameters_success(self, mock_cmdb_client_class):
        """Test successful retrieval of instance with two parameters"""
        # Arrange
        mock_client_instance = Mock()
        mock_cmdb_client_class.return_value = mock_client_instance
        
        expected_response = {
            'data': {
                'list': [
                    {
                        'instance_id': 'i-1234567890abcdef0',
                        'public_ip': '203.0.113.1',
                        'private_ip': '10.0.1.100',
                        'name': 'test-instance',
                        'status': 'running'
                    }
                ]
            }
        }
        mock_client_instance.get_assets.return_value = expected_response
        
        # Act
        result = self.get_instance_in_cmdb(
            instance_id='i-1234567890abcdef0', 
            public_ip='203.0.113.1', 
            private_ip=''
        )
        
        # Assert
        mock_cmdb_client_class.assert_called_once()
        mock_client_instance.get_assets.assert_called_once_with(
            catalog='vm',
            filters={
                'instance_id': 'i-1234567890abcdef0',
                'public_ip': '203.0.113.1'
            }
        )
        
        expected_result = {
            'provided': {
                'instance_id': 'i-1234567890abcdef0',
                'public_ip': '203.0.113.1'
            },
            'match_list': expected_response['data']['list']
        }
        self.assertEqual(result, expected_result)

    @patch('ops.mcp_tools_instance.CmdbClient')
    def test_get_instance_no_results_found(self, mock_cmdb_client_class):
        """Test when no instance is found"""
        # Arrange
        mock_client_instance = Mock()
        mock_cmdb_client_class.return_value = mock_client_instance
        
        expected_response = {
            'data': {
                'list': []
            }
        }
        mock_client_instance.get_assets.return_value = expected_response
        
        # Act
        result = self.get_instance_in_cmdb(instance_id='i-nonexistent', public_ip='', private_ip='')
        
        # Assert
        mock_cmdb_client_class.assert_called_once()
        mock_client_instance.get_assets.assert_called_once_with(
            catalog='vm',
            filters={'instance_id': 'i-nonexistent'}
        )
        
        expected_result = {
            'provided': {'instance_id': 'i-nonexistent'},
            'info': 'No information found.'
        }
        self.assertEqual(result, expected_result)

    @patch('ops.mcp_tools_instance.CmdbClient')
    def test_get_instance_empty_parameters(self, mock_cmdb_client_class):
        """Test with empty parameters"""
        # Arrange
        mock_client_instance = Mock()
        mock_cmdb_client_class.return_value = mock_client_instance
        
        expected_response = {
            'data': {
                'list': []
            }
        }
        mock_client_instance.get_assets.return_value = expected_response
        
        # Act
        result = self.get_instance_in_cmdb(instance_id='', public_ip='', private_ip='')
        
        # Assert
        mock_cmdb_client_class.assert_called_once()
        mock_client_instance.get_assets.assert_called_once_with(
            catalog='vm',
            filters={}
        )
        
        expected_result = {
            'provided': {},
            'info': 'No information found.'
        }
        self.assertEqual(result, expected_result)

    @patch('ops.mcp_tools_instance.CmdbClient')
    def test_get_instance_multiple_results(self, mock_cmdb_client_class):
        """Test when multiple instances are found"""
        # Arrange
        mock_client_instance = Mock()
        mock_cmdb_client_class.return_value = mock_client_instance
        
        expected_response = {
            'data': {
                'list': [
                    {
                        'instance_id': 'i-1234567890abcdef0',
                        'public_ip': '203.0.113.1',
                        'private_ip': '10.0.1.100',
                        'name': 'test-instance-1',
                        'status': 'running'
                    },
                    {
                        'instance_id': 'i-0987654321fedcba0',
                        'public_ip': '203.0.113.2',
                        'private_ip': '10.0.1.101',
                        'name': 'test-instance-2',
                        'status': 'running'
                    }
                ]
            }
        }
        mock_client_instance.get_assets.return_value = expected_response
        
        # Act
        result = self.get_instance_in_cmdb(instance_id='', public_ip='', private_ip='10.0.1.100')
        
        # Assert
        mock_cmdb_client_class.assert_called_once()
        mock_client_instance.get_assets.assert_called_once_with(
            catalog='vm',
            filters={'private_ip': '10.0.1.100'}
        )
        
        expected_result = {
            'provided': {'private_ip': '10.0.1.100'},
            'match_list': expected_response['data']['list']
        }
        self.assertEqual(result, expected_result)

    @patch('ops.mcp_tools_instance.CmdbClient')
    @patch('builtins.print')
    def test_get_instance_prints_results(self, mock_print, mock_cmdb_client_class):
        """Test that the function prints the results when found"""
        # Arrange
        mock_client_instance = Mock()
        mock_cmdb_client_class.return_value = mock_client_instance
        
        expected_response = {
            'data': {
                'list': [
                    {
                        'instance_id': 'i-1234567890abcdef0',
                        'public_ip': '203.0.113.1',
                        'private_ip': '10.0.1.100',
                        'name': 'test-instance',
                        'status': 'running'
                    }
                ]
            }
        }
        mock_client_instance.get_assets.return_value = expected_response
        
        # Act
        self.get_instance_in_cmdb(instance_id='i-1234567890abcdef0', public_ip='', private_ip='')
        
        # Assert
        mock_print.assert_called_once_with(expected_response['data']['list'])

    @patch('ops.mcp_tools_instance.CmdbClient')
    def test_get_instance_cmdb_client_exception(self, mock_cmdb_client_class):
        """Test handling of CmdbClient exceptions"""
        # Arrange
        mock_client_instance = Mock()
        mock_cmdb_client_class.return_value = mock_client_instance
        mock_client_instance.get_assets.side_effect = Exception("CMDB connection error")
        
        # Act & Assert
        with self.assertRaises(Exception) as context:
            self.get_instance_in_cmdb(instance_id='i-1234567890abcdef0', public_ip='', private_ip='')
        
        self.assertEqual(str(context.exception), "CMDB connection error")


if __name__ == '__main__':
    unittest.main()