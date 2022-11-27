import pandas as pd

from rdkit import Chem
from rdkit.Chem.Draw import rdMolDraw2D

__all__ = ['to_html']

__version__ = '0.0.1'

def _columns(target: str):
    return [
        'ID',
        'SMILES',
        f'{target}_from_smiles',
        f'{target}_to_smiles',
        f'{target}_avg',
    ]

def _load_template() -> str:
    return """
    <html>
        <style>
            .wrapper
            .content {
                width: 1024px;
                margin: 0px auto;
                padding: 64px 0px;
            }
            .content {
            }
            .h1-title {
            }
            .table {
            }
            .th {
            }
            .td {
            }
        </style>
        <body>
            <div class="wrapper">
                <div class="content">
                    <h1 class="h1-title">{_title_}</h1>
                    <table class="table">
                        {_table_header_}
                        {_table_content_}
                    </table>
                </div>
            </div>
        </body>
    </html>
    """

def _generate_header(target: str) -> str:
    row = '<tr>'
    for name in _columns(target):
        th = f'<th class=".th">{name}</th>'
        row += th
    row += '</tr>'
    return row

def _smiles_to_svg(smiles: str, size: int) -> str:
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return 'Failed to execute MolFromSmiles()'
    
    view = rdMolDraw2D.MolDraw2DSVG(size, size)
    view.DrawMolecule(mol)
    view.FinishDrawing()
    return view.GetDrawingText()

def _generate_content(df: pd.DataFrame, target: str) -> str:
    df_render = df[_columns(target)]
    values = df_render.values

    contents = ''
    for i in range(len(df_render)):
        row = '<tr>'
        fmt = '<td class=".td">{}</td>'
        row += fmt.format(str(values[i, 0])) # ID
        row += fmt.format(_smiles_to_svg(values[i, 1], 320)) # SMILES
        row += fmt.format(_smiles_to_svg(values[i, 2], 160)) # {}_from_SMILES
        row += fmt.format(_smiles_to_svg(values[i, 3], 160)) # {}_to_SMILES
        row += fmt.format(str(values[i, 4])) # {}_avg
        row += '</tr>'
        contents += row
    return contents

def to_html(df: pd.DataFrame, target: str) -> str:
    return _load_template()\
        .replace('{_title_}', target)\
        .replace('{_table_header_}', _generate_header(target))\
        .replace('{_table_content_}', _generate_content(df, target))
