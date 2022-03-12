# rptree.py
# -*- coding: utf-8 -*-    
"""This module provides RP Tree main module."""
import os
import pathlib

PIPE = "|"
ELBOW = "|--"
TEE = "|--"
PIPE_PREFIX = "|  "
SPACE_PREFIX = "   "


class DirectoryTree:  
    def __init__(self, root_dir): 
        self._generator = _TreeGenerator(root_dir)

    def generate(self):
        tree = self._generator.build_tree()
        for entry in tree:
            print(entry)


#defines _TreeGenerator
class _TreeGenerator:
    #defines class initializer, takes root dir as argument, holds tree's root directory path
    def __init__(self, root_dir):
        self._root_dir = pathlib.Path(root_dir)
        #defines empty list to store entities that shape directory tree
        self._tree = []

    #Generates and returns the directory tree diagram
    def build_tree(self):
        #build tree head
        self._tree_head()
        #generate the rest of the diagram
        self._tree_body(self._root_dir)
        return self._tree
    
    #Adds the name of root directory to ._tree, add PIPE to connect root directory
    def _tree_head(self):
        self._tree.append(f"{self._root_dir}{os.sep}")
        self._tree.append(PIPE)
    
    #define ._tree_body(), two arguments, directory hold the path to the directory you walk through
    #prefix holds the prefix string that you use to draw the tree diagram
    def _tree_body(self, directory, prefix=""):
        #calls on directory and assign result to entries, call returns an interator over the files in directory
        entries = directory.interdir()
        #checks the entries in directory using sorted(), lambda checks if its a file, returns true or false
        entries = sorted(entries, key=lambda entry: entry.is_file())
        #calls len() to get number of entries in the directory
        entries_count = len(entries)
        #starts a for loop to iterate over directory,enumerate() associates an index to each entry
        for index, entry in enumerate(entries):
            #defines connector symbol you'll use to draw the tree
            connector = ELBOW if index == entries_count - 1 else TEE
            #conditional which checks if entry is a directory
            if entry.is_dir():
                self._add_directory(
                        entry, index, entries_count, prefix, connector
                )
            else:
                self._add_file(entry, prefix, connector)

    #defines add directory
    def _add_directory(
            self, directory, index, entries_count, prefix, connector
    ):
        #adds new directory to ._tree
        self._tree.append(f"{prefix}{connector} {directory.name}{os.sep}")
        #runs conditional that updates prefix according to the index of current entry
        if index != entries_count - 1:
            prefix += PIPE_PREFIX
        else:
            prefix += SPACE_PREFIX
        #calls tree body with new set of arguments, indirect recursive call    
        self._tree_body(
            directory = directory,
            prefix = prefix,
        )
        #appends new prefix to seperate the content of current directory
        self._tree.append(prefix.rstrip())

    def _add_file(self, file, prefix, connector):
       self._tree.append(f"{prefix}{connector} {file.name}")
