#!/usr/bin/env python

# -*- coding: utf-8 -*-

import argparse
import json

from qdrant_client import QdrantClient
from qdrant_client.models import Filter
from qdrant_client.qdrant_fastembed import QueryResponse

from qdrant_example import get_dist_name, get_version


class encoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, QueryResponse):
            return o.__dict__
        return json.JSONEncoder.default(self, o)


def read_line(filepath):
    with open(filepath) as file:
        for line in file:
            yield line


def command_recreate(args):
    client = QdrantClient(host=args.host, port=args.port, https=False)
    client.set_model("intfloat/multilingual-e5-large")

    ok = client.recreate_collection(
        vectors_config=client.get_fastembed_vector_params(),
        collection_name=args.collection,
    )
    print(ok)


def command_add(args):
    ids = []
    docs = []
    metadata = []
    for line in read_line(args.file):
        dict = json.loads(line)
        ids.append(dict.pop("id"))
        docs.append(dict.pop("text"))
        metadata.append(dict)

    client = QdrantClient(host=args.host, port=args.port, https=False)
    client.set_model("intfloat/multilingual-e5-large")

    result = client.add(
        collection_name=args.collection,
        ids=ids,
        documents=docs,
        metadata=metadata,
        parallel=0,  # Use all available CPU cores to encode data s
    )
    print(result)


def command_query(args):
    client = QdrantClient(host=args.host, port=args.port, https=False)
    client.set_model("intfloat/multilingual-e5-large")

    search_result = client.query(
        collection_name=args.collection,
        query_text=args.query,
        query_filter=None
        if args.filter is None
        else Filter(**json.loads(args.filter)),
    )

    for item in search_result:
        # Delete "document" that is not necessary for display
        del item.metadata["document"]
        print(
            "id=%d document=%s metadata=%s score=%f"
            % (item.id, item.document, item.metadata, item.score)
        )


def command_help(args):
    print(args)


def main():
    # コマンドラインパーサーを作成
    parser = argparse.ArgumentParser(
        usage=get_dist_name(), description="Qdrant Command Line Interface"
    )
    parser.add_argument(
        "-v", "--version", action="store_true", help="show version"
    )
    subparsers = parser.add_subparsers()

    # create コマンドの parser を作成
    parser_recreate = subparsers.add_parser(
        "recreate", help="create collection"
    )
    parser_recreate.add_argument(
        "-H",
        "--host",
        metavar="<HOST>",
        type=str,
        default="localhost",
        help="host name",
    )
    parser_recreate.add_argument(
        "-p",
        "--port",
        metavar="<PORT>",
        type=int,
        default="6333",
        help="port number",
    )
    parser_recreate.add_argument(
        "collection", metavar="<COLLECTION_NAME>", help="collection name"
    )
    parser_recreate.set_defaults(handler=command_recreate)

    # add コマンドの parser を作成
    parser_add = subparsers.add_parser("add", help="upsert data")
    parser_add.add_argument(
        "-H",
        "--host",
        metavar="<HOST>",
        type=str,
        default="localhost",
        help="host name",
    )
    parser_add.add_argument(
        "-p",
        "--port",
        metavar="<PORT>",
        type=int,
        default="6333",
        help="port number",
    )
    parser_add.add_argument(
        "collection", metavar="<COLLECTION_NAME>", help="collection name"
    )
    parser_add.add_argument("file", metavar="<FILE>", help="file path")
    parser_add.set_defaults(handler=command_add)

    # query コマンドの parser を作成
    parser_query = subparsers.add_parser("query", help="search")
    parser_query.add_argument(
        "-H",
        "--host",
        metavar="<HOST>",
        type=str,
        default="localhost",
        help="host name",
    )
    parser_query.add_argument(
        "-p",
        "--port",
        metavar="<PORT>",
        type=int,
        default="6333",
        help="port number",
    )
    parser_query.add_argument(
        "-f",
        "--filter",
        metavar="<FILTER>",
        type=str,
        default=None,
        help="filter query",
    )
    parser_query.add_argument(
        "collection", metavar="<COLLECTION_NAME>", help="collection name"
    )
    parser_query.add_argument("query", metavar="<QUERY>", help="query text")
    parser_query.set_defaults(handler=command_query)

    # コマンドライン引数をパースして対応するハンドラ関数を実行
    args = parser.parse_args()

    if args.version:
        print(get_version())

    if hasattr(args, "handler"):
        args.handler(args)
    else:
        # 未知のサブコマンドの場合はヘルプを表示
        parser.print_help()


if __name__ == "__main__":
    main()
