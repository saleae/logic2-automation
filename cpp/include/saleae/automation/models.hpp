#ifndef SALEAE_AUTOMATION_APPINFO_HPP
#define SALEAE_AUTOMATION_APPINFO_HPP

#include <cstdint>
#include <optional>
#include <string_view>
#include <variant>
#include <vector>

namespace saleae::automation {

using ChannelIdx = std::size_t;

struct SemverVersion {
    std::uint64_t major;
    std::uint64_t minor;
    std::uint64_t patch;
};

struct LogicAppInfo {
    SemverVersion apiVersion;
    std::string_view appVersion;
    int appPid;
};

namespace device {
    namespace logic {
        enum class Type {
            Unspecified,
            Logic,
            Logic4,
            Logic8,
            Logic16,
            LogicPro8,
            LogicPro16,
            Count
        };

        struct Descriptor {
            std::string_view deviceId;
            Type deviceType;
            bool isSimulation;
        };

        struct Config {
            struct AnalogChannelCollection {
                std::uint64_t sampleRate;
                std::vector<ChannelIdx> enabledChannels;
            };

            struct DigitalChannelCollection {
                enum class VoltageThreshold {
                    Unspecified,
                    V1_2,
                    V1_8,
                    V3_3,
                    Count,
                };

                struct GlitchFilter {
                    ChannelIdx forChannel;
                    float pulseWidthSeconds;
                };

                std::uint64_t sampleRate;
                std::vector<ChannelIdx> enabledChannels;
                std::optional<VoltageThreshold> threshold = std::nullopt;
                std::vector<GlitchFilter> glitchFilters = {};
            };

            std::optional<AnalogChannelCollection> analogChannels = std::nullopt;
            std::optional<DigitalChannelCollection> digitalChannels = std::nullopt;
        };
    } // namespace logic

    using Config = std::variant<logic::Config>;
} // namespace device

namespace capture {
    struct DigitalTriggerMode {
        // TODO(markovejnovic): Figure out a way to pin against the pbuf
        // trigger types.
        enum class TriggerType {
            Unspecified,
            Rising,
            Falling,
            PulseHigh,
            PulseLow,
            Count,
        };

        struct LinkedChannel {
            // TODO(markovejnovic): Figure out a way to pin against the pbuf
            // trigger types.
            enum class LinkedChannelState {
                Unspecified,
                Low,
                High,
                Count,
            };

            std::size_t channelIndex;
            LinkedChannelState state;
        };

        TriggerType triggerType;
        ChannelIdx triggerChannelIndex;
        std::optional<float> minPulseWidthSeconds = std::nullopt;
        std::optional<float> maxPulseWidthSeconds = std::nullopt;
        std::vector<LinkedChannel> linkedChannels;
        std::optional<float> trimDataSeconds;
        std::optional<float> triggerDataSeconds;
    };
    struct TimedMode {
        float durationSeconds;
        std::optional<float> trimDataSeconds;
    };
    struct ManualMode {
        std::optional<float> trimDataSeconds;
    };

    using Mode = std::variant<DigitalTriggerMode, TimedMode, ManualMode>;

    struct Config {
        std::optional<int> bufferSizeMB;
        Mode captureMode;
    };
} // namespace capture

} // namespace saleae::automation

#endif // SALEAE_AUTOMATION_APPINFO_HPP
