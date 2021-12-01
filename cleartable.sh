table_name=forthepeople-app-826c4696-0908-44c6-9390-3db9776528d5

aws dynamodb describe-table --table-name $table_name | jq '.Table | del(.TableId, .TableArn, .ItemCount, .TableSizeBytes, .CreationDateTime, .TableStatus, .LatestStreamArn, .LatestStreamLabel, .ProvisionedThroughput.NumberOfDecreasesToday, .ProvisionedThroughput.LastIncreaseDateTime)' > schema.json
aws dynamodb delete-table --table-name $table_name
sleep 5
aws dynamodb create-table --cli-input-json file://schema.json
rm schema.json