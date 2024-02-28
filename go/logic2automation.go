//go:generate go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
//go:generate go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
//go:generate protoc --proto_path=. --go_out=. --go_opt=Msaleae.proto=github.com/saleae/logic2-automation/go;logic2automation --go_opt=paths=source_relative --go-grpc_out=. --go-grpc_opt=Msaleae.proto=github.com/saleae/logic2-automation/go;logic2automation --go-grpc_opt=paths=source_relative --proto_path ../proto/saleae/grpc/ ../proto/saleae/grpc/saleae.proto

package logic2automation
