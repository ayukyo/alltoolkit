// Example: Builder Pattern
// Demonstrates using JSON builders for efficient JSON construction
package main

import (
	"encoding/json"
	"fmt"

	"json_utils"
)

func main() {
	fmt.Println("=== JSON Builder Pattern Demo ===\n")

	// 1. Simple object with Buffer
	fmt.Println("1. Building Simple Object:")
	fmt.Println("--------------------------")
	buf := jsonutils.NewBuffer()
	simpleJSON := buf.StartObject().
		Key("name").AddString("John Doe").
		Key("age").Number(30).
		Key("email").AddString("john@example.com").
		Key("active").Bool(true).
		Key("score").Number(95.5).
		Key("data").Null().
		EndObject().
		String()

	fmt.Println(simpleJSON)
	fmt.Println()

	// 2. Building Array
	fmt.Println("2. Building Array:")
	fmt.Println("------------------")
	ab := jsonutils.NewArrayBuilder()
	arrayJSON := ab.
		Add("apple").
		Add("banana").
		Add("cherry").
		Add(42).
		Add(true).
		Add(nil).
		String()

	fmt.Println(arrayJSON)
	fmt.Println()

	// 3. Nested Objects using Merge
	fmt.Println("3. Building Nested Objects:")
	fmt.Println("---------------------------")
	// Build address object
	addressBuf := jsonutils.NewBuffer()
	addressJSON := addressBuf.StartObject().
		Key("street").AddString("123 Main St").
		Key("city").AddString("New York").
		Key("zip").AddString("10001").
		Key("country").AddString("USA").
		EndObject().
		String()

	// Build user object with nested address
	userBuf := jsonutils.NewBuffer()
	userJSON := userBuf.StartObject().
		Key("id").Number(1).
		Key("name").AddString("John Doe").
		Key("address").AddString(addressJSON).
		Key("active").Bool(true).
		EndObject().
		String()

	// Fix: address should not be quoted, use merge
	userObj := make(map[string]interface{})
	json.Unmarshal([]byte(userJSON), &userObj)
	
	// Parse address properly
	var addressObj interface{}
	json.Unmarshal([]byte(addressJSON), &addressObj)
	userObj["address"] = addressObj
	
	fixedUser, _ := json.Marshal(userObj)
	fmt.Println(string(fixedUser))
	fmt.Println()

	// 4. Building API Response
	fmt.Println("4. Building API Response:")
	fmt.Println("-------------------------")
	dataBuf := jsonutils.NewBuffer()
	dataJSON := dataBuf.StartObject().
		Key("id").Number(12345).
		Key("name").AddString("Sample Item").
		Key("price").Number(29.99).
		Key("inStock").Bool(true).
		EndObject().
		String()

	metaBuf := jsonutils.NewBuffer()
	metaJSON := metaBuf.StartObject().
		Key("page").Number(1).
		Key("pageSize").Number(10).
		Key("total").Number(100).
		EndObject().
		String()

	// Merge all parts
	response, _ := jsonutils.Merge(
		`{"success": true, "code": 200, "message": "Success"}`,
		`{"data": `+dataJSON+`}`,
		`{"meta": `+metaJSON+`}`,
	)

	pretty, _ := jsonutils.PrettyPrint(response, "  ")
	fmt.Println(pretty)
	fmt.Println()

	// 5. Building Dynamic List
	fmt.Println("5. Building Dynamic List:")
	fmt.Println("-------------------------")
	items := []struct {
		ID    int
		Name  string
		Price float64
	}{
		{1, "Laptop", 999.99},
		{2, "Mouse", 29.99},
		{3, "Keyboard", 79.99},
		{4, "Monitor", 299.99},
	}

	itemsBuilder := jsonutils.NewArrayBuilder()
	for _, item := range items {
		itemBuf := jsonutils.NewBuffer()
		itemJSON := itemBuf.StartObject().
			Key("id").Number(float64(item.ID)).
			Key("name").AddString(item.Name).
			Key("price").Number(item.Price).
			EndObject().
			String()

		var itemObj interface{}
		json.Unmarshal([]byte(itemJSON), &itemObj)
		itemsBuilder.Add(itemObj)
	}

	productsJSON := itemsBuilder.String()
	prettyProducts, _ := jsonutils.PrettyPrint(productsJSON, "  ")
	fmt.Println(prettyProducts)
	fmt.Println()

	// 6. Building Complex Report using Merge
	fmt.Println("6. Building Complex Report:")
	fmt.Println("---------------------------")
	summaryBuf := jsonutils.NewBuffer()
	summaryJSON := summaryBuf.StartObject().
		Key("totalUsers").Number(1500).
		Key("activeUsers").Number(1200).
		Key("newUsers").Number(300).
		Key("churnRate").Number(0.05).
		EndObject().
		String()

	metricsBuilder := jsonutils.NewArrayBuilder()
	metrics := []struct {
		Name   string
		Value  float64
		Change float64
	}{
		{"Revenue", 50000, 0.15},
		{"Orders", 1200, 0.08},
		{"Conversion", 3.2, -0.02},
	}
	for _, m := range metrics {
		metricBuf := jsonutils.NewBuffer()
		metricJSON := metricBuf.StartObject().
			Key("name").AddString(m.Name).
			Key("value").Number(m.Value).
			Key("change").Number(m.Change).
			EndObject().
			String()
		var metricObj interface{}
		json.Unmarshal([]byte(metricJSON), &metricObj)
		metricsBuilder.Add(metricObj)
	}

	report, _ := jsonutils.Merge(
		`{"reportId": "RPT-2024-001", "generatedAt": "2024-01-15T10:30:00Z"}`,
		`{"summary": `+summaryJSON+`}`,
		`{"metrics": `+metricsBuilder.String()+`}`,
		`{"status": "completed"}`,
	)

	prettyReport, _ := jsonutils.PrettyPrint(report, "  ")
	fmt.Println(prettyReport)
	fmt.Println()

	// 7. Building Error Response
	fmt.Println("7. Building Error Response:")
	fmt.Println("---------------------------")
	errorsBuilder := jsonutils.NewArrayBuilder()
	
	error1Buf := jsonutils.NewBuffer()
	error1JSON := error1Buf.StartObject().
		Key("field").AddString("email").
		Key("message").AddString("Invalid email format").
		Key("code").AddString("INVALID_EMAIL").
		EndObject().
		String()
	var error1Obj interface{}
	json.Unmarshal([]byte(error1JSON), &error1Obj)
	errorsBuilder.Add(error1Obj)

	error2Buf := jsonutils.NewBuffer()
	error2JSON := error2Buf.StartObject().
		Key("field").AddString("password").
		Key("message").AddString("Password too short").
		Key("code").AddString("PASSWORD_TOO_SHORT").
		EndObject().
		String()
	var error2Obj interface{}
	json.Unmarshal([]byte(error2JSON), &error2Obj)
	errorsBuilder.Add(error2Obj)

	errorResponse, _ := jsonutils.Merge(
		`{"success": false, "code": 400, "message": "Validation failed"}`,
		`{"errors": `+errorsBuilder.String()+`}`,
	)

	prettyError, _ := jsonutils.PrettyPrint(errorResponse, "  ")
	fmt.Println(prettyError)
	fmt.Println()

	fmt.Println("=== Demo Complete ===")
}
