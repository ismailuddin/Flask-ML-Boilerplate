// Load Grunt
module.exports = function (grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        sass: {
            dist: {
                options: {
                    style: 'expanded',
                    loadPath: ['node_modules/'],
                },
                files: {
                    './public/css/main.css' : './src/scss/main.scss',
                }
            }
        },
        watch: {
            css: {
                files: '**/*.scss',
                tasks: ['sass',]
            }
        },

    });

    // Load Grunt plugins
    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-contrib-watch');

    // Register Grunt tasks
    grunt.registerTask('build', ['sass']);
};
