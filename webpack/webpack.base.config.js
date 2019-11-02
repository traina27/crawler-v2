const path = require('path')
const webpack = require('webpack')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const WriteFilePlugin = require('write-file-webpack-plugin')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const dotenv = require('dotenv')

// Constant with our paths
const paths = {
  DIST: path.resolve(__dirname, '../dist'),
  SRC: path.resolve(__dirname, '../web'),
  JS: path.resolve(__dirname, '../web/js')
}

// Webpack configuration
const webpackConfig = {
  entry: path.join(paths.SRC, 'index.js'),
  output: {
    path: paths.DIST,
    publicPath: '/',
    filename: 'app.[hash].bundle.js',
  },
  // Tell webpack to use html plugin
  plugins: [
    new WriteFilePlugin(),
    new HtmlWebpackPlugin({
      template: path.join(paths.SRC, 'index.html'),
      inject: true,
      chunksSortMode: 'none'
    }),
    new MiniCssExtractPlugin({
      filename: '[name].[hash].css',
      chunkFilename: '[id].[hash].css'
    }),
    new webpack.ProvidePlugin({
      $: 'jquery',
      jQuery: 'jquery',
      'window.jQuery': 'jquery',
      Popper: ['popper.js', 'default'],
    })
  ],
  // devServer: {
  //   host: 'system-admin.vxlocate.local',
  //   historyApiFallback: true,
  //   watchOptions: {
  //     ignored: /node_modules/,
  //     poll: true
  //   }
  // },
  // Loaders configuration
  // We are telling webpack to use "babel-loader" for .js and .jsx files
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: [
          'babel-loader',
          'eslint-loader'
        ],
      },
      // CSS loader for CSS files
      // Files will get handled by css loader and then passed to the extract text plugin
      // which will write it to the file we defined above
      {
        test: /\.(s?css)$/,
        exclude: /node_modules/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          'sass-loader'
        ]
      },
      // File loader for image assets -> ADDED IN THIS STEP
      // We'll add only image extensions, but you can things like svgs, fonts and videos
      {
        test: /\.(png|jpg|gif|ico)$/,
        use: [
          'file-loader',
        ],
      },
      {
        test: /\.(woff|woff2|eot|ttf|otf|svg)$/,
        use: ['file-loader']
      }
    ],
  },
  resolve: {
    extensions: ['.js', '.jsx'],
    alias: {
      jquery: path.join(__dirname, '../node_modules/jquery/dist/jquery'),
      actions: path.resolve(__dirname, '../src/actions'),
      components: path.resolve(__dirname, '../src/components'),
      containers: path.resolve(__dirname, '../src/containers'),
      constants: path.resolve(__dirname, '../src/constants'),
      reducers: path.resolve(__dirname, '../src/reducers'),
      store: path.resolve(__dirname, '../src/store'),
      api: path.resolve(__dirname, '../src/api'),
      styles: path.resolve(__dirname, '../src/styles'),
      routes: path.resolve(__dirname, '../src/routes'),
      pages: path.resolve(__dirname, '../src/pages'),
      i18n: path.resolve(__dirname, '../src/i18n'),
      utils: path.resolve(__dirname, '../src/utils'),
      translations: path.resolve(__dirname, '../src/translations'),
      assets: path.resolve(__dirname, '../src/assets'),
      sagas: path.resolve(__dirname, '../src/sagas'),
      layouts: path.resolve(__dirname, '../src/layouts'),
    },
  },
  node: {
    fs: 'empty',
    tls: 'empty',
  }
}

module.exports = (env) => {
  const environment = dotenv.config().parsed
  const envKeys = Object.keys(environment).reduce((prev, next) => ({
    ...prev,
    [`process.env.${next}`]: JSON.stringify(environment[next])
  }), {})

  const BASE_API_URL = 'process.env.BASE_API_URL'
  const POOL_ID = 'process.env.POOL_ID'
  const IOT_HOST = 'process.env.IOT_HOST'
  const REGION = 'process.env.REGION'
  switch (env.NODE_ENV) {
    case 'stg':
      envKeys[BASE_API_URL] = envKeys[`${BASE_API_URL}_STG`]
      break
    case 'prod':
      envKeys[BASE_API_URL] = envKeys[`${BASE_API_URL}_PROD`]
      envKeys[POOL_ID] = envKeys[`${POOL_ID}_PROD`]
      envKeys[IOT_HOST] = envKeys[`${IOT_HOST}_PROD`]
      envKeys[REGION] = envKeys[`${REGION}_PROD`]
      break
    default:
      break
  }

  webpackConfig.plugins.push(new webpack.DefinePlugin(envKeys))

  return webpackConfig
}
