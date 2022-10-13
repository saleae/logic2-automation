def build_protobufs(root_proto_dir: str):
    import grpc_tools.protoc
    import os.path

    print("Building logic2-automation protobuf files")

    args = [
        'protoc',
        '-I', root_proto_dir,
        '--python_out=./',
        '--grpc_python_out=./',
        os.path.join(root_proto_dir, 'saleae/grpc/saleae.proto')
    ]
    grpc_tools.protoc.main(args)

if __name__ == '__main__':
    build_protobufs('../proto')
else:
    from hatchling.builders.hooks.plugin.interface import BuildHookInterface
    class CustomBuildHook(BuildHookInterface):
        def initialize(self, version, build_data):
            build_protobufs('./proto')

