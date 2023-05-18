const BundleTracker = require("webpack-bundle-tracker");

module.exports = {
    publicPath:
        process.env.NODE_ENV === "development"
            ? "http://localhost:9000/static/smiles/dist/"
            : "/static/smiles/dist/",
    outputDir: "../smiles/static/smiles/dist",
    pages: {
         app: "src/main"
    },
    configureWebpack: {
        plugins: [
            new BundleTracker({
                filename: "webpack-stats.json",
                path: "../smiles/static/smiles/dist/"
            })
        ],
        optimization: {
            /*
             * Force creating a vendor bundle so we can load the 'app' and 'vendor'
             * bundles on development as well as production using django-webpack-loader.
             * Otherwise there is no vendor bundle on development and we would need
             * some template logic to skip trying to load it.
             * See also: https://bitbucket.org/calidae/dejavu/src/d63d10b0030a951c3cafa6b574dad25b3bef3fe9/%7B%7Bcookiecutter.project_slug%7D%7D/frontend/vue.config.js?at=master&fileviewer=file-view-default#vue.config.js-27
             */
            splitChunks: {
                cacheGroups: {
                    vendors: {
                        name: 'chunk-vendors',
                        test: /[\\/]node_modules[\\/]/,
                        priority: -10,
                        chunks: 'initial'
                    },
                    // there is only one entry point so common chunk isn't needed
                    //   common: {
                    //     name: 'chunk-common',
                    //     minChunks: 2,
                    //     priority: -20,
                    //     chunks: 'initial',
                    //     reuseExistingChunk: true
                    //   }
                }
            }
        },
        devServer: {
            port: 9000,
            headers: {
                "Access-Control-Allow-Origin": "*"
            },
            hot: true,
        }
    }
}
