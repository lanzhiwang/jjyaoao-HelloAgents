# 全端 LLM 應用開發 - Day21 - 用 Qdrant 儲存向量資料

* https://ithelp.ithome.com.tw/m/articles/10335513

昨天我們談了 Qdrant 的優勢, 以及和其他向量資料庫的比較. 還有一點我昨天忘記講的是, 微軟的 Semantic Kernel 在推出沒多久時, 就選擇了和 Qdrant 合作. 可以知道 Qdrant 是一個相當有潛力的向量資料庫. 今天我們就來教怎麼架設和使用吧!

## 環境設定

1. 使用 docker compose 來在本地端架起來吧! 使用下面的程式碼, 建立檔案 `docker-compose.yml`, 然後接著用指令 `docker-compose up -d` 來跑起來.

```yml
version: '3'
services:
  qdrant:
    image: qdrant/qdrant
    restart: always
    ports:
      - '6333:6333'
    volumes:
      - ./qdrant_storage:/qdrant/storage
```

2. 接著我們進到 localhost:6333, 就會看到 `{"title":"qdrant - vector search engine","version":"1.1.3"}`, 這樣子代表成功了.

3. 接著我們安裝 Qdrant 的 Python SDK, 使用指令 `poetry add qdrant-client`

4. 如果你在安裝 python sdk 時有出現下面錯誤, 可以把 `pyproject.toml` 裡的 python 固定版本, 而不要使用 `^`. 例如說你可以固定為 `3.11.5`. 然後再執行 `poetry update`

```
Check your dependencies Python requirement: The Python requirement can be specified via the `python` or `markers` properties

    For qdrant-client, a possible solution would be to set the `python` property to ">=3.11,<3.12"
```

## Qdrant 使用

Qdrant 的 collection 的觀念, 和 Milvus 比較相近. 我們在使用時, 就是把向量資料存在 collection 裡面, 但是不用像 Milvus 要先定義 schema.

1. 建立一個 python 檔 `qdrant_tutorial.py`, 先連線到 Qdrant 資料庫.

```python
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import PointStruct

client = QdrantClient("http://localhost:6333")
```

2. 接著我們建立一個 `collection`, 這裡`向量長度`一樣使用 1536, 並且用 `cosine` 來算相似度. 注意這裡我們用了 `OptimizersConfigDiff` 來優化搜尋, 讓資料可以 load 進 memory 跑. 然後我們使用 `HnswConfigDiff`, `m` 是 Maximum degree of the node, 愈大會愈準但是更花資料, 而 `ef_construct` 是 Search scope, 並且可以把 hnsw 的索引儲存在硬碟上. 程式碼改寫如下:

```python
COLLECTION_NAME = "Lyrics"


def connection():
    client = QdrantClient("http://localhost:6333")

    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        # 建立一個 collection, 這裡向量長度一樣使用 1536, 並且用 cosine 來算相似度
        vectors_config=models.VectorParams(distance=models.Distance.COSINE, size=1536),
        # OptimizersConfigDiff 來優化搜尋, 讓資料可以 load 進 memory 跑
        optimizers_config=models.OptimizersConfigDiff(memmap_threshold=20000),
        # HnswConfigDiff
        # m 是 Maximum degree of the node, 愈大會愈準但是更花資料,
        # 而 ef_construct 是 Search scope, 並且可以把 hnsw 的索引儲存在硬碟上
        hnsw_config=models.HnswConfigDiff(on_disk=True, m=16, ef_construct=100),
    )
    return client
```

3. 接著我們一樣放入向量資料.

```python
def get_embedding(text, model_name):
    response = openai.Embedding.create(input=text, engine=model_name)
    return response["data"][0]["embedding"]
```

4. 建立一個 function 是插入資料到 Qdrant. 昨天提到 Qdrant 的 metadata 概念是 payload, 這裡我們可以放入 json, 而 vector 的部份就插入 embedding 後的向量. 值得一提的是, 一個 `points` 可以放入多個 PointStruct, 就是昨天提到一個 point 可以存多個向量, 這也是 Qdrant 的特性. 舉例來說, 圖片做 embedding, 該圖片的描述做 embedding. 這種應用場景很常見, 而且是兩個一組的 embedding. 如果要做這種應用的話, Qdrant 就非常方便. 不過這裡我們就只放入文字的向量.

```python
def upsert_vector(client, vectors, data):
    for i, vector in enumerate(vectors):
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=[PointStruct(id=i, vector=vectors[i], payload=data[i])],
        )

    print("upsert finish")
```

5. 再來建立一個 search 的 function. 一般都會設定 `append_payload=True`, 這樣子可以把存進去的 json 一起帶出來.

```python
def search_from_qdrant(client, vector, k=1):
    search_result = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=vector,
        limit=k,
        append_payload=True,
    )
    return search_result
```

6. 接著就是我們的主程式了.

```python
def main():

    EMBEDDING_MODEL_NAME = "embedding-ada-002"
    openai.api_base = "https://japanopenai2023ironman.openai.azure.com/"
    openai.api_key = "yourkey"
    openai.api_type = "azure"
    openai.api_version = "2023-03-15-preview"

    qclient = connection()

    data_objs = [
        {
            "id": 1,
            "lyric": "我會披星戴月的想你, 我會奮不顧身的前進, 遠方煙火越來越唏噓, 凝視前方身後的距離",
        },
        {
            "id": 2,
            "lyric": "而我, 在這座城市遺失了你, 順便遺失了自己, 以為荒唐到底會有捷徑. 而我, 在這座城市失去了你, 輸給慾望高漲的自己, 不是你, 過分的感情",
        },
    ]
    embedding_array = [
        get_embedding(text["lyric"], EMBEDDING_MODEL_NAME) for text in data_objs
    ]

    upsert_vector(qclient, embedding_array, data_objs)

    query_text = "工程師寫城市"
    query_embedding = get_embedding(query_text, EMBEDDING_MODEL_NAME)
    results = search_from_qdrant(qclient, query_embedding, k=1)
    print(f"尋找 {query_text}:", results)


if __name__ == "__main__":
    main()

```

跑了之後, 就會得到結果如下.

```bash
尋找 工程師寫城市:
[
    ScoredPoint(
        id=1,
        version=1,
        score=0.79302907,
        payload={
            'id': 2,
            'lyric': '而我, 在這座城市遺失了你, 順便遺失了自己, 以為荒唐到底會有捷徑. 而我, 在這座城市失去了你, 輸給慾望高漲的自己, 不是你, 過分的感情'
        },
        vector=None
    )
]
```

Qdrant 的使用是不是也很簡單呢! Qdrant 還有很多進階的使用, 不過礙於篇幅的關係, 我們向量資料庫已經談了九天. 明天開始進到 embedding 後的下個階段, RAG!
