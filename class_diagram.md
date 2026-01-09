```mermaid
classDiagram
    class Shared <<Module>> {
        +camera: TapoCamera
        +video_streamer: VideoStreamer
        +audio_streamer: AudioStreamer
        +recorder: Recorder
    }

    class TapoCamera {
        +ip: string
        +user: string
        +password: string
        +cloudPassword: string
        +connect()
        +read_frame()
        +move(direction, step)
        +release()
    }

    class VideoStreamer {
        +is_running: bool
        +motion_active: bool
        +start_streaming()
    }

    class AudioStreamer {
        +is_running: bool
        +start_streaming()
    }

    class BaseDetector {
        <<Abstract>>
        +detect(frame)*
    }

    class MotionDetector {
        +min_area: int
        +detect(frame)
    }

    class Recorder {
        +is_recording: bool
        +start_recording()
        +add_frame(frame)
        +add_audio(audio_data)
        +stop_recording()
    }

    Shared o-- TapoCamera
    Shared o-- VideoStreamer
    Shared o-- AudioStreamer
    Shared o-- Recorder

    VideoStreamer --> TapoCamera : uses
    VideoStreamer --> MotionDetector : uses
    AudioStreamer --> TapoCamera : uses
    MotionDetector --|> BaseDetector : inherits

    VideoStreamer ..> Shared : uses
    AudioStreamer ..> Shared : uses
```
Powyższy kod w formacie Mermaid reprezentuje zaktualizowany diagram klas dla Twojej aplikacji, uwzględniając obiekty współdzielone.

**Główne zmiany:**

-   **Moduł `Shared`**: Dodano klasę `Shared` ze stereotypem `<<Module>>`, aby przedstawić plik `app/shared.py`. Przechowuje on globalnie dostępne instancje głównych klas (`TapoCamera`, `VideoStreamer`, `AudioStreamer`, `Recorder`). Relacja kompozycji (`o--`) pokazuje, że te obiekty są częścią `Shared`.
-   **Relacje z `Shared`**: Klasy `VideoStreamer` i `AudioStreamer` mają teraz relację `uses` (pokazaną jako przerywana linia `..>`) z modułem `Shared`. Oznacza to, że uzyskują dostęp do współdzielonych obiektów (w tym przypadku `Recorder`) za pośrednictwem tego modułu, a nie bezpośrednio.

Dzięki temu diagram dokładniej odzwierciedla architekturę aplikacji, gdzie centralny moduł `shared` zarządza kluczowymi obiektami i udostępnia je innym częściom systemu.
