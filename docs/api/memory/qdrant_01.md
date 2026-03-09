# 全端 LLM 應用開發 - Day20 - 為什麼 Qdrant 是我儲存向量資料的主力

* https://ithelp.ithome.com.tw/m/articles/10334900

我們談了 FAISS、pgvector、Pinecone、Milvus、Weaviate 等儲存向量資料的方方式, 但是我實務上最常使用的向量資料庫反而是 Qdrant.

## 強大的效能

Qdrant 讀做 `quadrant`, 也是一套開源的向量資料庫, 使用 `Rust` 開發. Qdrant 的效能非常好, 我們可以看到他們做的 [benchmark](https://qdrant.tech/benchmarks/), 可以發現他幾乎屌打其他的向量資料庫. 這裡幫我總結一下.

- 索引時間:

Qdrant 與 Milvus, 兩者在索引時間方面表現出色. 他們建立內部搜尋結構的速度遠高於其他引擎.

- 請求每秒(RPS)與延遲:

Qdrant 在幾乎所有情境中, 不論所選擇的精確度閾值和測量方式, Qdrant 都達到了最高的 RPS 和最低的延遲.

- 多段索引:

有些引擎嘗試創建單一的 HNSW 索引, 而有些則採用多段索引. 單一段索引會帶來更高的 RPS, 但精確度較低且索引時間較長. Qdrant 允許您配置段數, 以達到所需目標.

- Redis 的性能:

當只使用一個 thread 時, Redis 的效能優於其他引擎. 但由於其結構上僅限於單一線程執行, 所以它無法垂直擴展.

- Elasticsearch 的性能:

不論資料集和測量方式, Elasticsearch 通常比所有競爭者都慢.

## 至於另一個龍頭 pinecone 呢?

之前的介紹我們也提到了 Pinecone 可以說是目前向量資料庫的龍頭, 但是我還是選擇了 Qdrant, 這是為什麼呢?

最致命的原因就是 Pinecone 只提供了 SaaS 服務, 而 Qdrant 有 SaaS 服務, 也可以開源在本地端自架. 雖然在雲的年代、全託管已經是很常見的概念了, 但是 Qdrant 在部署的彈性是大很多.

還有錢的問題. Pinecone 每月 70 美元起, 而 Qdrant 是 25 美元. 前幾天我們在做 Pinecone 的向量資料時, 大家應該有發現免費版本的速度還滿慢的吧? 如果為了好一點的 demo 與測試, 每個月要花到 70 美元, 對於獨立開發者來說會是一個負擔. 而 Qdrant 只要 25 美元就有全託管的版本了, 免費版的效能也很不錯, 更別提 Qdrant 也可以一個 docker compose 就在本地端跑起來了.

一個 point 可以存多個向量, 這也是 Qdrant 的特性. 舉例來說, 圖片做 embedding, 該圖片的描述做 embedding. 這種應用場景很常見, 而且是兩個一組的 embedding. 如果要做這種應用的話, Qdrant 就非常方便, 這也是 Pinecone 所不支援的, 要 workaround.

因此我目前在實務上多是使用 Qdrant 來做開發. 明天我們來就來用 Qdrant 吧!
