Documentor
==========

Documentation generation tool for Python.
Documentor scan all the source code of your project and generate a documentation 
site with the collected information of your project using Nikola.

# **Ninja-ide** | Ninja-ide Is Not Just Another IDE.

Ninja-IDE is a cross-platform integrated development environment (IDE) that runs
on Linux/X11, Mac OS X and Windows desktop operating systems. Ninja-IDE allows
developers to create applications for any purpose making the task of writing
software easier and more enjoyable.

# The code in repository is NOT working right now, we are integrating the changes and doing lot of improves for the new Architecture!!

## Contact

-   [Homepage](https://github.com/diegosarmentero/documentor) at github.com/diegosarmentero/documentor
-   [@ninja\_ide](https://twitter.com/diegosarmentero) at Twitter
-   [#ninja-ide](irc://freenode.net/ninja-ide) at Freenode.net (I'm always here :P)

## Dependencies

Both of these:

-   [Python](http://python.org/) >= 2.7 (or Python3)
-   [Nikola](http://nikola.ralsina.com.ar/)


## Cloning and Running

(You need to install NIKOLA first!)
You can clone this repo and simply execute:

    git clone https://github.com/diegosarmentero/documentor.git
    cd documentor
    python documentor.py -p path/to/project -o /output/path

Piece of cake, uh?
(Soon the setup.py will be ready to be able to execute this even more easily)

### Optional Arguments:

*usage:*
```bash
documentor.py [-h] [-p project] [-o Output Folder]
              [--projectname projectname] 
              [--email email]
              [--serve False/True: default False]

$documentor -p project_path -o output_path [--projectname name, --email address --serve=True/False]

- "serve" can take "output" as the project which need to be served as documentation


optional arguments:
  -h, --help            show this help message and exit
  -p project, --project project
                        Create documentation for this project
  -o Output Folder, --output Output Folder
                        Place to locate the outpur result
  --projectname projectname
                        Project Name, if not provided the name is
                        generatedusing: documentor_PATHBASENAME
  --email email         email address of the project
  --serve False/True: default False
                        Serve Documentation site
```

## Video Demonstration

http://youtu.be/z9CAKfst66A

## License

-   GPL v3
