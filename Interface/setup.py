from cx_Freeze import setup, Executable

# On appelle la fonction setup
setup(
    name = "test",
    version = "1.0",
    description = "chose qui mesure les molécules",
    executables = [Executable("main.py")],
)