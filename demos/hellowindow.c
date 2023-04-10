#include <SDL2/SDL.h>

int main(int argc, char* argv[]) {
    SDL_Window* window = NULL; // Declare a window pointer
    SDL_Init(SDL_INIT_VIDEO); // Initialize SDL2

    // Create a window with the desired settings
    window = SDL_CreateWindow("Pascal", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, 640, 480, SDL_WINDOW_OPENGL);

    // Check that the window was successfully created
    if (window == NULL) {
        // In the case that the window could not be made...
        printf("Could not create window: %s\n", SDL_GetError());
        return 1;
    }

    // Event loop
    while (1) {
        SDL_Event event;
        if (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                break;
            }
        }
        // Render the window contents here
    }

    // Destroy window
    SDL_DestroyWindow(window);

    // Quit SDL2
    SDL_Quit();

    return 0;
}