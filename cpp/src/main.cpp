#include <grpc++/grpc++.h>

#include "saleae/grpc/saleae.pb.h"
#include "saleae/grpc/saleae.grpc.pb.h"

#include <memory>

using namespace saleae::automation;

int main()
{
    auto client = std::make_unique<Manager::Stub>(
        grpc::CreateChannel("127.0.0.1:50051", grpc::InsecureChannelCredentials()));

    grpc::ClientContext context;

    LoadCaptureRequest request;
    LoadCaptureReply reply;
    auto status = client->LoadCapture(&context, request, &reply);

    return 0;
}