## 1. Examine the tree command. Master the technique of applying a template, for example, display all files that contain a character c, or files that contain a specific sequence of characters. List subdirectories of the root directory up to and including the second nesting level. ##

tree command lists contents of directories in a tree-like format. To list only thosefiles that match the wild-card pattern, use the following command:
  tree -P pattern
And to max display depth of the directory tree, use:
  tree -L level
  
![alt text]()

## 2. What command can be used to determine the type of file (for example, text or binary)? Give an example. ##

To determine the type if file, use file command. file tests each arfument in an attempt to classify it:
  
![alt text]()

## 3. Master the skills of navigating the file system using relative and absolute paths. How can you go back to your home directory from anywhere in the filesystem?  ##

An absolute path is defined as the specifying the location of a file or directory from the root directory(/). In other words we can say absolute path is a complete path from start of actual filesystem from / directory.
Relative path is defined as path related to the present working directory(pwd).

![alt text]()

To go back to your home directory from anywhere in the filesystem, use:
  cd ~
  
 or 
  cd
  

 

