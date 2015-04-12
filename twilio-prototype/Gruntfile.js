js_files = ["Gruntfile.js", "client/javascript/**/*.js", "server.js", "routes/**/*.js", "models/**/*.js", "config/**/*.js"];

module.exports = function(grunt) {
  grunt.initConfig({
    pkg: grunt.file.readJSON("package.json"),

    sass: {
      dist: {
        options: {
          style:"compressed"
        },
        files: {
          "client/stylesheets/style.css" : "sass/main.scss"
        }
      }
    },

    jshint: {
      all: js_files
    },

    watch: {
      options: {
        livereload: true,
      },

      scripts: {
        files: js_files,
        tasks: ["jshint"],
        options: {
          spawn: false
        }
      },

      css: {
        files: ["sass/*.scss"],
        tasks: ["sass"],
        options: {
          spawn: false
        }
      }
    }
  });

  require('load-grunt-tasks')(grunt);
  grunt.registerTask("default", ["sass", "jshint", "watch"]);
};
