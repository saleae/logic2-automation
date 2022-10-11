from hatchling.builders.hooks.plugin.interface import BuildHookInterface
import grpc_tools.protoc

class CustomBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        print("Building logic2-automation protobuf files")
        args = [
            'protoc',
            '-I', './proto',
            '--python_out=./',
            '--grpc_python_out=./',
            './proto/saleae/grpc/saleae.proto'
        ]
        grpc_tools.protoc.main(args)

