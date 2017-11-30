from cx_Freeze import setup, Executable

setup(
    name="GerarXML",
    version = "1.0.0",
    author="LINX S.A",
    author_email="gabriel.pires@linx.com.br / ygohr.campos@linx.com.br",
    description = ".Projeto Gerar XML Estoque e ReducaoZ",
    executables = [Executable("GerarXML.py")])

