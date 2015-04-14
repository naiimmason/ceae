js_files = ["Gruntfile.js", "client/javascript/**/*.js", "app.js", "routes/**/*.js", "models/**/*.js", "config/**/*.js"];

module.exports = function(grunt) {
  grunt.initConfig({
    pkg: grunt.file.readJSON("package.json"),

    jshint: {
      all: js_files
    },

    stylus: {
      compile: {
        options: {

        },
        files: {
          'client/stylesheets/style.css': 'stylus/main.styl'
        }
      }
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
        files: ["stylus/*.styl"],
        tasks: ["stylus"],
        options: {
          spawn: false
        }
      }
    }
  });

  require('load-grunt-tasks')(grunt);
  grunt.registerTask("default", ["jshint", "stylus","watch"]);
};
