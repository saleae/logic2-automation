#ifndef SALEAE_AUTOMATION_PRIVATE_GRPC_ADAPTERS_HPP
#define SALEAE_AUTOMATION_PRIVATE_GRPC_ADAPTERS_HPP

#include "saleae/automation/capture.hpp"
#include "saleae/automation/models.hpp"
#include "saleae/automation/private/utils.hpp"
#include "saleae/grpc/saleae.pb.h"
#include <algorithm>
#include <stdexcept>
#include <variant>

namespace saleae::automation {

inline auto Serialize(
    device::logic::Config::DigitalChannelCollection::VoltageThreshold threshold
) -> double {
    using VT =
        device::logic::Config::DigitalChannelCollection::VoltageThreshold;
    switch (threshold) {
        case VT::V1_2: return 1.2;
        case VT::V1_8: return 1.8;
        case VT::V3_3: return 3.3;

        case VT::Count:
            throw std::runtime_error(
                "Cannot serialize a \"Count\" voltage threshold."
            );
        case VT::Unspecified:
            throw std::runtime_error(
                "Cannot serialize an unspecified voltage threshold."
            );
    }
}

inline auto Serialize(
    const capture::DigitalTriggerMode::TriggerType trigger
) -> DigitalTriggerType {
    using InT = capture::DigitalTriggerMode::TriggerType;
    using OutT = DigitalTriggerType;

    switch (trigger) {
        case InT::Falling: return OutT::DIGITAL_TRIGGER_TYPE_FALLING;
        case InT::Rising: return OutT::DIGITAL_TRIGGER_TYPE_RISING;
        case InT::PulseHigh: return OutT::DIGITAL_TRIGGER_TYPE_PULSE_HIGH;
        case InT::PulseLow: return OutT::DIGITAL_TRIGGER_TYPE_PULSE_LOW;
        case InT::Unspecified: return OutT::DIGITAL_TRIGGER_TYPE_UNSPECIFIED;
                               
        case InT::Count:
            throw std::runtime_error(
                "Cannot serialize a \"Count\" trigger type."
            );
    }
}

inline auto Serialize(
    const capture::DigitalTriggerMode::LinkedChannel::LinkedChannelState in
) -> DigitalTriggerLinkedChannelState {
    using InT = capture::DigitalTriggerMode::LinkedChannel::LinkedChannelState;
    using OutT = DigitalTriggerLinkedChannelState;

    switch (in) {
        case InT::Unspecified:
            return OutT::DIGITAL_TRIGGER_LINKED_CHANNEL_STATE_UNSPECIFIED;
        case InT::Low:
            return OutT::DIGITAL_TRIGGER_LINKED_CHANNEL_STATE_LOW;
        case InT::High:
            return OutT::DIGITAL_TRIGGER_LINKED_CHANNEL_STATE_HIGH;
        case InT::Count:
            throw std::runtime_error(
                "Cannot serialize a \"Count\" linked channel type."
            );
    }
}

inline auto Serialize(
    const capture::Config& in
) -> CaptureConfiguration* {
    CaptureConfiguration* out = new CaptureConfiguration();

    if (in.bufferSizeMB.has_value()) {
        out->set_buffer_size_megabytes(*in.bufferSizeMB);
    }

    std::visit(overloaded{
        [&out](const capture::DigitalTriggerMode& mode) mutable {
            auto* modeOut = out->mutable_digital_capture_mode();
            modeOut->set_trigger_type(Serialize(mode.triggerType));
            if (mode.triggerDataSeconds.has_value()) {
                modeOut->set_after_trigger_seconds(*mode.triggerDataSeconds);
            }

            modeOut->set_trim_data_seconds(mode.trimDataSeconds.value_or(0));
            modeOut->set_trigger_channel_index(mode.triggerChannelIndex);

            if (mode.minPulseWidthSeconds.has_value()) {
                modeOut->set_min_pulse_width_seconds(
                    *mode.minPulseWidthSeconds);
            }

            if (mode.maxPulseWidthSeconds.has_value()) {
                modeOut->set_max_pulse_width_seconds(
                    *mode.maxPulseWidthSeconds);
            }

            for (const auto& chan : mode.linkedChannels) {
                auto* chanOut = modeOut->add_linked_channels();
                chanOut->set_channel_index(chan.channelIndex);
                chanOut->set_state(Serialize(chan.state));
            }
        },
        [&out](const capture::TimedMode& mode) mutable {
            auto* modeOut = out->mutable_timed_capture_mode();
            modeOut->set_duration_seconds(mode.durationSeconds);
            if (mode.trimDataSeconds.has_value()) {
                modeOut->set_trim_data_seconds(*mode.trimDataSeconds);
            }
        },
        [&out](const capture::ManualMode& mode) mutable {
            auto* modeOut = out->mutable_manual_capture_mode();
            if (mode.trimDataSeconds.has_value()) {
                modeOut->set_trim_data_seconds(*mode.trimDataSeconds);
            }
        }
    }, in.captureMode);

    return out;
}

inline auto Serialize(
    const device::logic::Config& config
) -> LogicDeviceConfiguration* {
    using device::logic::Config;

    LogicDeviceConfiguration* out = new LogicDeviceConfiguration();

    if (config.digitalChannels.has_value()) {
        using DVoltThreshold =
            Config::DigitalChannelCollection::VoltageThreshold;

        out->set_digital_sample_rate(config.digitalChannels->sampleRate);

        if (config.digitalChannels->threshold.has_value()) {
            out->set_digital_threshold_volts(
                Serialize(*config.digitalChannels->threshold)
            );
        }

        for (const auto& gf : config.digitalChannels->glitchFilters) {
            auto* gfOut = out->add_glitch_filters();
            gfOut->set_channel_index(gf.forChannel);
            gfOut->set_pulse_width_seconds(gf.pulseWidthSeconds);
        }

        for (const auto chan : config.digitalChannels->enabledChannels) {
            out->mutable_logic_channels()->add_digital_channels(chan);
        }
    }

    if (config.analogChannels.has_value()) {
        const auto& aChannels = config.analogChannels.value();
        out->set_analog_sample_rate(aChannels.sampleRate);

        for (const auto chan : config.analogChannels->enabledChannels) {
            out->mutable_logic_channels()->add_analog_channels(chan);
        }
    }

    return out;
}

inline auto Deserialize(const GetAppInfoReply& reply) -> LogicAppInfo {
    const auto& appInfo = reply.app_info();

    return {
        .apiVersion = {
            .major = appInfo.api_version().major(),
            .minor = appInfo.api_version().minor(),
            .patch = appInfo.api_version().patch(),
        },
        .appVersion = appInfo.application_version(),
        .appPid = static_cast<int>(appInfo.launch_pid()),
    };
}

inline auto Deserialize(
    const GetDevicesReply& reply
) -> std::vector<device::logic::Descriptor> {
    const auto& devices = reply.devices();

    std::vector<device::logic::Descriptor> output;
    output.reserve(devices.size());

    std::transform(
        devices.cbegin(), devices.cend(), output.begin(),
        [](const Device& dev) {
            return device::logic::Descriptor {
                .deviceId = dev.device_id(),
                .deviceType = static_cast<device::logic::Type>(dev.device_type()),
                .isSimulation = dev.is_simulation(),
            };
        }
    );

    return output;
}

} // namespace saleae::automation

#endif // SALEAE_AUTOMATION_PRIVATE_GRPC_ADAPTERS_HPP
