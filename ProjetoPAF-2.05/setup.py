from cx_Freeze import setup, Executable

setup(
    name="GerarXML",
    version = "1.0.0",
    author="Gabriel Guimarães / Ygohr Medeiros",
    description = ".Projeto Gerar XML Estoque e ReducaoZ",
    executables = [Executable("GerarXML.py")])

