module.exports = function (grunt) {
  grunt
    .initConfig({
      "couch-compile": {
        dbs: {
          files: {
            "/tmp/food_twitters.json": "MyCouchdb/food_twitters/designs",
            "/tmp/job_twitters.json": "MyCouchdb/job_twitters/designs",
            "/tmp/shopping_twitters.json": "MyCouchdb/shopping_twitters/designs"
          }
        }
      },
      "couch-push": {
        options: {
          user: process.env.user,
          pass: process.env.pass
        },
        twitter: {
          files: {
            // "http://admin:123456@localhost:5984/aurin": "/tmp/aurin.json",
            "http://admin:123456@localhost:5984/food_twitters": "/tmp/food_twitters.json",
            "http://admin:123456@localhost:5984/job_twitters": "/tmp/job_twitters.json",
            "http://admin:123456@localhost:5984/shopping_twitters": "/tmp/shopping_twitters.json"
          }
        }
      }
    });

  grunt.loadNpmTasks("grunt-couch");
};
