#!/bin/bash

if [ 0 -eq $# ]; then
	echo "Usage: deploy book"
	exit
fi

book=$1
echo "Deploy book "$book"..."

echo "gitbook init.."
gitbook init $book

echo "gitbook build "$book" to "share/$book"..."
gitbook build $book share/$book

echo "deploy share to "flyingwjw.github.io"..."
cp -rf share ../flyingwjw.github.io
