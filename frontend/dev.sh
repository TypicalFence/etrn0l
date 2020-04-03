if [ ! -d "./dist" ] ; then
    yarn build
fi

yarn dev-server
