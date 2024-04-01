import os
from time import sleep
from subprocess import call
from dotenv import load_dotenv
from neo4j import GraphDatabase
# from neomodel import db

from django.test.runner import DiscoverRunner

class Neo4jTestRunner(DiscoverRunner):
    def setup_databases(self, *args, **kwargs):
        # Stop your development instance
        # call("sudo service neo4j-service stop", shell=True)
        # Sleep to ensure the service has completely stopped
        # sleep(1)
        # # Start your test instance (see section below for more details)
        # success = call("/path/to/test/db/neo4j-community-2.2.2/bin/neo4j"
        #                " start-no-wait", shell=True)
        # # Need to sleep to wait for the test instance to completely come up
        # sleep(10)
        # if success != 0:
        #     return False
        # try:
        #     # For neo4j 2.2.x you'll need to set a password or deactivate auth
        #     # Nigel Small's py2neo gives us an easy way to accomplish this
        #     call("source /path/to/virtualenv/bin/activate && "
        #          "/path/to/virtualenv/bin/neoauth "
        #          "neo4j neo4j my-p4ssword")
        # except OSError:
        #     pass
        # # Don't import neomodel until we get here because we need to wait 
        # # for the new db to be spawned
        # from neomodel import db
        # Delete all previous entries in the db prior to running tests
        load_dotenv()
        NEO4J_TEST_USERNAME = os.getenv('NEO4J_TEST_USERNAME')
        NEO4J_TEST_PASSWORD = os.getenv('NEO4J_TEST_PASSWORD')
        NEO4J_TEST_URI = os.getenv('NEO4J_TEST_URI')
        
        query = """MATCH (n) OPTIONAL MATCH (n)-[r]->()
                   DELETE n, r"""
        driver = GraphDatabase().driver(NEO4J_TEST_URI, auth=(NEO4J_TEST_USERNAME, NEO4J_TEST_PASSWORD))
        from neomodel import db
        db.set_connection(driver=driver)

        db.cypher_query(query)
        super(Neo4jTestRunner, self).__init__(*args, **kwargs)

    def teardown_databases(self, old_config, **kwargs):
        # Delete all previous entries in the db after running tests
        load_dotenv()
        NEO4J_TEST_USERNAME = os.getenv('NEO4J_TEST_USERNAME')
        NEO4J_TEST_PASSWORD = os.getenv('NEO4J_TEST_PASSWORD')
        NEO4J_TEST_URI = os.getenv('NEO4J_TEST_URI')
        
        query = """MATCH (n) OPTIONAL MATCH (n)-[r]->()
                   DELETE n, r"""
        driver = GraphDatabase().driver(NEO4J_TEST_URI, auth=(NEO4J_TEST_USERNAME, NEO4J_TEST_PASSWORD))
        from neomodel import db

        db.set_connection(driver=driver)
        db.cypher_query(query)

        # Get variables for Aura DB
        # load_dotenv()
        # NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
        # NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')
        # NEO4J_URI = os.getenv('NEO4J_URI')
        
        # driver = GraphDatabase().driver(NEO4J_TEST_URI, auth=(NEO4J_TEST_USERNAME, NEO4J_TEST_PASSWORD))
        # db.set_connection(driver=driver)

        # db.cypher_query(query)
                
        # sleep(1)
        # # Shut down test neo4j instance
        # success = call("/path/to/test/db/neo4j-community-2.2.2/bin/neo4j"
        #                " stop", shell=True)
        # if success != 0:
        #     return False
        # sleep(1)
        # # start back up development instance
        # call("sudo service neo4j-service start", shell=True)