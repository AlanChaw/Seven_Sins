module.exports = function (grunt) {
  grunt
    .initConfig({
      "couch-compile": {
        dbs: {
          files: {
            "/tmp/twitter.json": "couchdb/twitter/myDesign"
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
            "http://admin:123@localhost:5984/twitter": "/tmp/twitter.json"
          }
        }
      }
    });

  grunt.loadNpmTasks("grunt-couch");
};
