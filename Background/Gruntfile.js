module.exports = function (grunt) {
  grunt
    .initConfig({
      "couch-compile": {
        dbs: {
          files: {
            "/tmp/aurin.json": "MyCouchdb/aurin/myDesign",
            "/tmp/analysed_twitters.json": "MyCouchdb/analysed_twitters/designs"
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
            "http://admin:123456@localhost:5984/aurin": "/tmp/aurin.json",
            "http://admin:123456@localhost:5984/analysed_twitters": "/tmp/analysed_twitters.json"
          }
        }
      }
    });

  grunt.loadNpmTasks("grunt-couch");
};
