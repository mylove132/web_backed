import time

from kazoo.client import KazooClient

from kazoo.client import KazooState

zk = KazooClient(hosts='10.10.6.3:2181')
zk.start()


@zk.ChildrenWatch("/dubbo/com.noriental.solr.service.index.CoursewareSolrIndexServiceExt/providers")
def watch_children(children):
    print("Children are now: %s" % children)

# def main():
#
#     @zk.add_listener
#     def my_listener(state):
#
#         if state == KazooState.LOST:
#
#             print("LOST")
#
#         elif state == KazooState.SUSPENDED:
#
#             print("SUSPENDED")
#
#         else:
#
#             print("Connected")
#
#     # Creating Nodes
#
#     # Ensure a path, create if necessary
#
#     zk.ensure_path("/my/favorite")
#
#     # Create a node with data
#
#     zk.create("/my/favorite/node", b"")
#
#     zk.create("/my/favorite/node/a", b"A")
#
#     # Reading Data
#
#     # Determine if a node exists
#
#     if zk.exists("/my/favorite"):
#         print("/my/favorite is existed")
#
#
#
#     # Above function called immediately, and from then on
#
#     @zk.DataWatch("/my/favorite/node")
#     def watch_node(data, stat):
#
#         print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))
#
#     # Print the version of a node and its data
#
#     data, stat = zk.get("/my/favorite/node")
#
#     print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))
#
#     # List the children
#
#     children = zk.get_children("/my/favorite/node")
#
#     print("There are %s children with names %s" % (len(children), children))
#
#     # Updating Data
#
#     zk.set("/my/favorite", b"some data")
#
#     # Deleting Nodes
#
#     zk.delete("/my/favorite/node/a")
#
#     # Transactions
#
#     transaction = zk.transaction()
#
#     transaction.check('/my/favorite/node', version=-1)
#
#     transaction.create('/my/favorite/node/b', b"B")
#
#     results = transaction.commit()
#
#     print("Transaction results is %s" % results)
#
#     zk.delete("/my/favorite/node/b")
#
#     zk.delete("/my", recursive=True)
#
#     time.sleep(2)
#
#     zk.stop()