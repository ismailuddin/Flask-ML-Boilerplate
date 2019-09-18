const path = require('path');
const MiniCssExtractPluguin = require('mini-css-extract-plugin');

module.exports = {
    mode: process.env.NODE_ENV === 'production' ? 'production' : 'development',
    entry: {
        main: './src/scss/main.scss',
        table: './src/ts/table.ts'
    },
    output: {
        path: path.resolve(__dirname, 'public/'),
        filename: 'js/[name].js',
        libraryTarget: 'var',
        library: 'ML'
    },
    module: {
        rules: [
            {
                test: /\.(ts|js)$/,
                use: 'ts-loader',
                exclude: /node_modules/
            },
            {
                test: /\.(png|svg|jpe?g|gif)$/i,
                loader: 'file-loader',
                options: {
                    publicPath: '../svg/',
                    outputPath: 'svg/',
                    useRelativePaths: true
                },
            },
            {
                test: /\.scss$/,
                use: [
                    {
                        loader: MiniCssExtractPluguin.loader,
                    },
                    {
                        loader: 'css-loader',
                        options: {
                            sourceMap: true
                        }
                    },
                    {
                        loader: 'postcss-loader',
                        options: {
                            plugins: [
                                require('tailwindcss'),
                                require('autoprefixer')
                            ]
                        }
                    },
                    {
                        loader: 'sass-loader',
                        options: {
                            sourceMap: true
                        }
                    }
                ]
            }
        ]
    },
    plugins: [
        new MiniCssExtractPluguin({
            filename: 'css/[name].css',
            chunkFilename: 'css/[id].css'
        })
    ],
    watch: true
};