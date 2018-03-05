'''
Created on 21/02/2018

@author: David
'''
import unittest
import hscrap.global_vars
import os

class Test(unittest.TestCase):
    """Test class for module global_vars. It collects all variables that
    need to be known to many modules across the system"""

    def test_global_vars_url_setter_getter(self):
        """Tests getter and setter of url attribute"""
        g_ref = hscrap.global_vars.GlobalVars()
        var_to_set = "https://www.google.com"
        g_ref.set_url(var_to_set)
        self.assertEqual(g_ref.get_url(), var_to_set)
        
    def test_set_url_only_accepts_str(self):
        """Tests that it only accepts str instances, and raises Exception"""
        g_ref = hscrap.global_vars.GlobalVars()
        with self.assertRaises(Exception):
            var_to_set = 15
            g_ref.set_url(var_to_set)
    
    def test_global_vars_pages_setter_getter(self):
        """Tests getter and setter of no_pages attribute"""
        g_ref = hscrap.global_vars.GlobalVars()
        var_to_set = 1
        g_ref.set_no_pages(var_to_set)
        self.assertEqual(g_ref.get_no_pages(), var_to_set)
    
    def test_set_pages_only_accepts_int(self):
        """Tests that it only accepts int instances, and raises Exception"""
        g_ref = hscrap.global_vars.GlobalVars()
        with self.assertRaises(Exception):
            var_to_set = "hi!"
            g_ref.set_no_pages(var_to_set)
            
    def test_global_vars_out_path_setter_getter(self):
        """Tests getter and setter of out_path attribute"""
        g_ref = hscrap.global_vars.GlobalVars()
        var_to_set = os.path.dirname(__file__)+"\\"
        g_ref.set_out_path(var_to_set)
        self.assertEqual(g_ref.get_out_path(), var_to_set)
    
    def test_set_out_path_only_accepts_str(self):
        """Tests that it only accepts str instances, and raises Exception"""
        g_ref = hscrap.global_vars.GlobalVars()
        with self.assertRaises(Exception):
            var_to_set = 15
            g_ref.set_out_path(var_to_set)
            
    def test_global_vars_wait_time_setter_getter(self):
        """Tests getter and setter of no_pages attribute"""
        g_ref = hscrap.global_vars.GlobalVars()
        var_to_set = 1
        g_ref.set_wait_time(var_to_set)
        self.assertEqual(g_ref.get_wait_time(), var_to_set)
    
    def test_set_wait_time_only_accepts_int(self):
        """Tests that it only accepts int instances, and raises Exception"""
        g_ref = hscrap.global_vars.GlobalVars()
        with self.assertRaises(Exception):
            var_to_set = "hi!"
            g_ref.set_wait_time(var_to_set)
            

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()