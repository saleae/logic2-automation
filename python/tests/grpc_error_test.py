from saleae.grpc import saleae_pb2
import saleae.automation


def test_all_error_codes_have_exceptions():
  # Find error codes that don't map to an exception
  unmapped_error_codes = set(saleae_pb2.ErrorCode.values()).difference(saleae.automation.grpc_error_code_to_exception_type.keys())

  assert len(unmapped_error_codes) == 0, f'All error codes should map to an exception. Unmapped error codes: {", ".join(str(code) for code in unmapped_error_codes)}'
