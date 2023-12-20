#ifndef SALEAE_AUTOMATION_APPINFO_HPP
#define SALEAE_AUTOMATION_APPINFO_HPP

#include <optional>
#include <string_view>
#include <variant>
#include <vector>

namespace saleae::automation {

using ChannelIdx = std::size_t;

struct SemverVersion {
    unsigned long major;
    unsigned long minor;
    unsigned long patch;
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
                unsigned long long sampleRate;
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

                unsigned long long sampleRate;
                std::vector<ChannelIdx> enabledChannels;
                VoltageThreshold threshold;
                std::vector<GlitchFilter> glitchFilters = {};
            };

            std::optional<AnalogChannelCollection> analogChannels = std::nullopt;
            std::optional<DigitalChannelCollection> digitalChannels = std::nullopt;
        };
    };

    using Config = std::variant<logic::Config>;
};

namespace capture {
    class DigitalTriggerMode {
    public:
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

            size_t channelIndex;
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
    class TimedMode {
        float durationSeconds;
        std::optional<float> trimDataSeconds;
    };
    class ManualMode {
        std::optional<float> trimDataSeconds;
    };

    using Mode = std::variant<DigitalTriggerMode, TimedMode, ManualMode>;

    struct Config {
        std::optional<int> bufferSizeMB;
    };
};

} // namespace saleae::automation

#endif // SALEAE_AUTOMATION_APPINFO_HPP
