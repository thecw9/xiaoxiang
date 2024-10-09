package utils

import (
	"bytes"
	"database/sql"
	"encoding/json"
	"fmt"
	"net/http"
	"strings"
	"sync"
	"time"

	"push_layer_go/config"
)

// KeyInfo 定义了关键字信息的结构
type KeyInfo struct {
	Key     string
	Unit    string
	Name    string
	Path    string
	Quality int
}

// RealTimeData 定义了实时数据的结构
type RealTimeData struct {
	Key       string
	Value     float64
	Time      string
	FreshTime string
}

// GetKeyInfoByKeywords 根据包含和排除的关键词获取键信息
func GetKeyInfoByKeywords(db *sql.DB, include []string, exclude []string) ([]KeyInfo, error) {
	whereClauses := []string{}

	if len(include) > 0 {
		includeConditions := []string{}
		for _, i := range include {
			includeConditions = append(includeConditions, fmt.Sprintf("path LIKE '%%%s%%'", i))
		}
		whereClauses = append(whereClauses, strings.Join(includeConditions, " AND "))
	}

	if len(exclude) > 0 {
		excludeConditions := []string{}
		for _, e := range exclude {
			excludeConditions = append(excludeConditions, fmt.Sprintf("path NOT LIKE '%%%s%%'", e))
		}
		excludeClause := strings.Join(excludeConditions, " AND ")
		whereClauses = append(whereClauses, excludeClause)
	}

	whereClause := ""
	if len(whereClauses) > 0 {
		whereClause = "WHERE " + strings.Join(whereClauses, " AND ")
	}

	query := fmt.Sprintf(`
        SELECT id, unitsymbol, name, path, quality
        FROM analog
        %s
    `, whereClause)

	rows, err := db.Query(query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var results []KeyInfo
	for rows.Next() {
		var id sql.NullString
		var unitsymbol sql.NullString
		var name sql.NullString
		var path sql.NullString
		var quality sql.NullInt64

		err = rows.Scan(&id, &unitsymbol, &name, &path, &quality)
		if err != nil {
			return nil, err
		}
		result := KeyInfo{
			Key:     id.String,
			Unit:    unitsymbol.String,
			Name:    name.String,
			Path:    path.String,
			Quality: int(quality.Int64),
		}
		results = append(results, result)
	}
	return results, nil
}

// FetchRealTimeDataFromAPI 从 API 获取实时数据
func FetchRealTimeDataFromAPI(keys []string) ([]RealTimeData, error) {
	url := "http://192.168.4.117/v1/cs/realdata-service/data/realtime"
	headers := map[string]string{
		"X-HW-ID":       "your-hw-id",   // 请替换为实际的 X-HW-ID
		"X-HW-APPKEY":   "your-app-key", // 请替换为实际的 X-HW-APPKEY
		"User-Agent":    "Apifox/1.0.0 (https://apifox.com)",
		"Content-Type":  "application/json",
		"Authorization": "Bearer your-token", // 请替换为实际的令牌
	}

	var values []RealTimeData

	for i := 0; i < len(keys); i += 1000 {
		end := i + 1000
		if end > len(keys) {
			end = len(keys)
		}
		keysChunk := keys[i:end]
		payload := map[string]interface{}{
			"id":       1,
			"clientId": "serv-x01",
			"body": map[string]interface{}{
				"datatype": "analog",
				"keys":     keysChunk,
			},
		}

		payloadBytes, err := json.Marshal(payload)
		if err != nil {
			return nil, err
		}

		req, err := http.NewRequest("POST", url, bytes.NewBuffer(payloadBytes))
		if err != nil {
			return nil, err
		}

		for k, v := range headers {
			req.Header.Set(k, v)
		}

		client := &http.Client{}
		resp, err := client.Do(req)
		if err != nil {
			return nil, err
		}
		defer resp.Body.Close()

		var jsonResp struct {
			Body struct {
				Values []struct {
					Key       interface{} `json:"key"`
					Value     float64     `json:"value"`
					TimeStamp string      `json:"time_stamp"`
					FreshTime string      `json:"fresh_time"`
				} `json:"values"`
			} `json:"body"`
		}

		err = json.NewDecoder(resp.Body).Decode(&jsonResp)
		if err != nil {
			return nil, err
		}

		for _, v := range jsonResp.Body.Values {
			data := RealTimeData{
				Key:       fmt.Sprintf("%v", v.Key),
				Value:     v.Value,
				Time:      strings.Replace(v.TimeStamp, " ", "T", -1),
				FreshTime: strings.Replace(v.FreshTime, " ", "T", -1),
			}
			values = append(values, data)
		}
	}

	return values, nil
}

// currentDataIndex 用于记录当前数据索引
var currentDataIndex = make(map[string]int)
var currentDataIndexMutex sync.Mutex

// FetchRealTimeDataMock 从数据库模拟获取实时数据
func FetchRealTimeDataMock(db *sql.DB, keys []string) ([]RealTimeData, error) {
	// 获取所有以 "scada_analogueother" 开头的表名
	statement := `
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_name LIKE 'scada_analogueother%'
    `
	rows, err := db.Query(statement)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var tables []string
	for rows.Next() {
		var tableName string
		err = rows.Scan(&tableName)
		if err != nil {
			return nil, err
		}
		if tableName != "scada_analogueother202310" {
			tables = append(tables, tableName)
		}
	}

	var results []RealTimeData

	for _, key := range keys {
		// 构建计数查询
		unionQueries := []string{}
		for _, table := range tables {
			unionQueries = append(unionQueries, fmt.Sprintf("SELECT COUNT(*) FROM %s WHERE attr_oid = %s", table, key))
		}
		countQuery := strings.Join(unionQueries, " UNION ALL ")
		countRows, err := db.Query(countQuery)
		if err != nil {
			return nil, err
		}

		var counts []int
		for countRows.Next() {
			var count int
			err = countRows.Scan(&count)
			if err != nil {
				return nil, err
			}
			counts = append(counts, count)
		}
		countRows.Close()

		total := 0
		tablesExistData := []string{}
		for i, count := range counts {
			if count > 0 {
				tablesExistData = append(tablesExistData, tables[i])
				total += count
			}
		}

		// 更新 currentDataIndex
		currentDataIndexMutex.Lock()
		currentDataIndex[key] = currentDataIndex[key] + 1
		currentDataIndex[key] = currentDataIndex[key] % total
		currentIndex := currentDataIndex[key]
		currentDataIndexMutex.Unlock()

        // 构建数据查询，明确指定需要的列，并将 attr_oid 转换为文本类型
        unionDataQueries := []string{}
        for _, table := range tablesExistData {
            unionDataQueries = append(unionDataQueries, fmt.Sprintf("SELECT attr_oid::text, fvalue, attr_time FROM %s WHERE attr_oid = %s", table, key))
        }
        dataQuery := strings.Join(unionDataQueries, " UNION ALL ") + fmt.Sprintf(" ORDER BY attr_time LIMIT 1 OFFSET %d", currentIndex)

        dataRows, err := db.Query(dataQuery)
        if err != nil {
            return nil, err
        }

        if dataRows.Next() {
            var attr_oid sql.NullString
            var fvalue float64
            var attr_time time.Time

            // 扫描查询结果的三列
            err = dataRows.Scan(&attr_oid, &fvalue, &attr_time)
            if err != nil {
                return nil, err
            }

            // 检查 attr_oid 是否为有效值
            if !attr_oid.Valid {
                return nil, fmt.Errorf("attr_oid is null")
            }

            dataRow := RealTimeData{
                Key:       attr_oid.String,
                Value:     fvalue,
                Time:      time.Now().Add(-6 * 24 * time.Hour).Format(time.RFC3339),
                FreshTime: attr_time.Format(time.RFC3339),
            }
            results = append(results, dataRow)
        }
        dataRows.Close()
    }

    return results, nil

}

// FetchRealTimeData 根据环境选择获取实时数据的方式
func FetchRealTimeData(cfg *config.Config, keys []string) ([]RealTimeData, error) {
	if cfg.Environment == "production" {
		return FetchRealTimeDataFromAPI(keys)
	} else {
		return FetchRealTimeDataMock(cfg.DB, keys)
	}
}

// MergeData 合并两个数据列表
func MergeData(arr1 []KeyInfo, arr2 []RealTimeData, key string) []map[string]interface{} {
	map1 := make(map[string]KeyInfo)
	for _, item := range arr1 {
		map1[item.Key] = item
	}

	map2 := make(map[string]RealTimeData)
	for _, item := range arr2 {
		map2[item.Key] = item
	}

	var merged []map[string]interface{}
	for k, v1 := range map1 {
		if v2, ok := map2[k]; ok {
			m := map[string]interface{}{
				"key":        v1.Key,
				"unit":       v1.Unit,
				"name":       v1.Name,
				"path":       v1.Path,
				"quality":    v1.Quality,
				"value":      v2.Value,
				"time":       v2.Time,
				"fresh_time": v2.FreshTime,
			}
			merged = append(merged, m)
		}
	}
	return merged
}
