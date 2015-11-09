package main

import (
	"errors"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"

	"gopkg.in/mgo.v2"
	"gopkg.in/yaml.v2"
)

type handler struct {
	confFilename string
}

func (h *handler) ServeHTTP(w http.ResponseWriter, _ *http.Request) {
	url, err := mongoUrlFromConf(h.confFilename)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	session, err := mgo.Dial(url)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	names, err := session.DatabaseNames()
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	for _, name := range names {
		w.Write([]byte(name))
		w.Write([]byte("\n"))
	}
}

func mongoUrlFromConf(filename string) (string, error) {
	f, err := ioutil.ReadFile(filename)
	if err != nil {
		return "", err
	}
	conf := map[string]string{}
	err = yaml.Unmarshal(f, conf)
	if err != nil {
		return "", err
	}
	if _, ok := conf["mongo-url"]; !ok {
		return "", errors.New(fmt.Sprintf("missing mongo-url %q", conf))
	}
	return conf["mongo-url"], nil
}

func main() {
	flag.Parse()
	conf := flag.Args()[0]
	log.Fatal(http.ListenAndServe(":8080", &handler{conf}))
}
