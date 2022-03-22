# mcapt
([mediapipe](https://github.com/google/mediapipe)) を利用した手の軌道追跡

- **Windows 11** 環境で開発中 (WSL / WSL2 では**使用不可**)

## インストール
### 注意
- Python 3.10 のみ対応
- poetry による仮想環境使用

> Poetry のインストール
```sh
python -m pip install -U pip setuptools
python -m pip install poetry
python -m poetry shell
```

> 依存ライブラリーのインストール
```sh
poetry install
```

## 実行
```sh
python mcapt/mcapt.py
```
