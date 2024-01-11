# Create daily task OpenProject

- [Create daily task OpenProject](#create-daily-task-openproject)
  - [概要](#概要)
  - [準備](#準備)
  - [実行](#実行)
  - [参考](#参考)

## 概要

OpenProjectに日次タスクを追加する。

## 準備

1. `app/config/parent_task.json`に親タスクの情報を記載する。
    - `$date$`と記載している箇所が、起動時に引数で渡された文字列に置換される。
2. `app/config/child_task.json`に子タスクの情報を記載する。
    - `$date$`と記載している箇所が、起動時に引数で渡された文字列に置換される。
3. `app/src/sample.env`をコピーして、`app/src/.env`を作成する。
4. `app/src/.env`に`API_KEY`と`ENDPOINT`を記載する。
5. venv環境を作成する。
    ``` bash
    python -m venv venv
    source venv/bin/activate

    # 必要なライブラリをインストールする
    pip install -r app/requirements/requirements.txt

    deactivate
    ```

## 実行

``` bash
bash start_venv.sh ${task_date}
```

## 参考

- [API Endpoints : OpenProject](https://www.openproject.org/docs/api/endpoints/)
    - [work_packages](https://www.openproject.org/docs/api/endpoints/work-packages/)