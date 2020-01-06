package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"net/http"
	"os"
	"strings"
)

//  "resultCode": 0,
//  "resultMessage": "Account created",

const (
	version   = "0.1v"
	url       = "https://<hostname>/api.php"
	authtoken = "<auth_token>"
	tokenpass = "<token_password>"
)

type aResponse struct {
	Jsonrpc string `json:"jsonrpc"`
	Result  struct {
		ItemID int `json:"itemId"`
		Result struct {
			ID                 int         `json:"id"`
			UserID             int         `json:"userId"`
			UserGroupID        int         `json:"userGroupId"`
			UserEditID         int         `json:"userEditId"`
			Name               string      `json:"name"`
			ClientID           int         `json:"clientId"`
			CategoryID         int         `json:"categoryId"`
			Login              string      `json:"login"`
			URL                string      `json:"url"`
			Pass               string      `json:"pass"`
			Key                string      `json:"key"`
			Notes              string      `json:"notes"`
			OtherUserEdit      string      `json:"otherUserEdit"`
			OtherUserGroupEdit string      `json:"otherUserGroupEdit"`
			DateAdd            string      `json:"dateAdd"`
			DateEdit           interface{} `json:"dateEdit"`
			CountView          int         `json:"countView"`
			CountDecrypt       int         `json:"countDecrypt"`
			IsPrivate          string      `json:"isPrivate"`
			IsPrivateGroup     string      `json:"isPrivateGroup"`
			PassDate           int         `json:"passDate"`
			PassDateChange     int         `json:"passDateChange"`
			ParentID           int         `json:"parentId"`
			CategoryName       string      `json:"categoryName"`
			ClientName         string      `json:"clientName"`
			UserGroupName      string      `json:"userGroupName"`
			UserName           string      `json:"userName"`
			UserLogin          string      `json:"userLogin"`
			UserEditName       string      `json:"userEditName"`
			UserEditLogin      string      `json:"userEditLogin"`
			PublicLinkHash     interface{} `json:"publicLinkHash"`
		} `json:"result"`
		ResultCode    int         `json:"resultCode"`
		ResultMessage string      `json:"resultMessage"`
		Count         interface{} `json:"count"`
	} `json:"result"`
	ID int `json:"id"`
}

func newAcnt(aurl string, aname string, alogin string, apass string) int {
	// Define structure of the response
	method := "POST"
	payload := strings.NewReader("{\n  \"jsonrpc\": \"2.0\",\n  \"method\": \"account/create\",\n  \"params\": {\n    \"authToken\": \"" + authtoken + "\",\n    \"tokenPass\": \"" + tokenpass + "\",\n    \"name\": \"" + aname + "\",\n    \"categoryId\": \"1\",\n    \"clientId\": \"1\",\n    \"login\": \"" + alogin + "\",\n    \"pass\": \"" + apass + "\",\n    \"url\": \"" + aurl + "\"\n  },\n  \"id\": 1\n}")

	client := &http.Client{}
	req, err := http.NewRequest(method, url, payload)
	if err != nil {
		fmt.Println("Issue with compiling body")
		os.Exit(2)
	}

	req.Header.Add("Content-Type", "application/json")

	res, err := client.Do(req)
	if err != nil {
		fmt.Println("Issue with connection")
		os.Exit(3)
	}

	defer res.Body.Close()

	var val aResponse
	// byteValue, _ := ioutil.ReadAll(res.Body)

	json.NewDecoder(res.Body).Decode(&val)

	if val.Result.ResultCode != 0 {
		fmt.Printf("Failed to add new ID")
		os.Exit(4)
	}
	return val.Result.ItemID
}

func main() {

	aurl := flag.String("u", "", "Provide URL to be stored with password")
	aname := flag.String("n", "", "Name for the new pasasword account")
	alogin := flag.String("l", "", "Login used for new account")
	apass := flag.String("p", "", "Login password for new account")

	flag.Parse()

	if *aname == "" && *alogin == "" && *apass == "" {
		fmt.Println("Provide Name, Login and password, e.g. -n=<string> -l=<string> -p=<string>")
		fmt.Println("Optionally you can define URL to go with account : -u=<url>")
		os.Exit(1)
	}

	newID := newAcnt(*aurl, *aname, *alogin, *apass)
	fmt.Printf("Entry Added: %d\n", newID)
}
