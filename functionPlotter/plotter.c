#include <SDL2/SDL.h>
#include <stdio.h>
#include "tinyexpr.h"

#define WIDTH 800
#define HEIGHT 600

#define THICKNESS 3

void draw_grid(SDL_Surface *surface) {
    SDL_Color grid_color = {211, 211, 211, 50};
    int grid_spacing = 50;

    for (int x = 0; x < WIDTH; x += grid_spacing) {
        SDL_Rect line = {x, 0, 1, HEIGHT};
        SDL_FillRect(surface, &line, SDL_MapRGB(surface->format, grid_color.r, grid_color.g, grid_color.b));
    }

    for (int y = 0; y < HEIGHT; y += grid_spacing) {
        SDL_Rect line = {0, y, WIDTH, 1};
        SDL_FillRect(surface, &line, SDL_MapRGB(surface->format, grid_color.r, grid_color.g, grid_color.b));
    }
}

void draw_axes(SDL_Surface *surface) {
    SDL_Color axis_color = {255, 0, 0, 255};

    // Draw X axis
    SDL_Rect x_axis = {0, HEIGHT / 2, WIDTH, 1};
    SDL_FillRect(surface, &x_axis, SDL_MapRGB(surface->format, axis_color.r, axis_color.g, axis_color.b));

    // Draw Y axis
    SDL_Rect y_axis = {WIDTH / 2, 0, 1, HEIGHT};
    SDL_FillRect(surface, &y_axis, SDL_MapRGB(surface->format, axis_color.r, axis_color.g, axis_color.b));
}

void draw_expression(SDL_Surface *surface, const char *expression) {
    double x;  // variable used in expression

    te_variable vars[] = {
        {"x", &x, TE_VARIABLE, NULL}
    };

    int error;
    te_expr *expr = te_compile(expression, vars, 1, &error);
    if (!expr) {
        printf("Error compiling expression at position: %d\n", error);
        return;
    }

    SDL_Color func_color = {0, 0, 0, 255};

    double step = 0.1; // step size for plotting

    for (double i = -WIDTH / 2.0; i < WIDTH / 2.0; i += step) {
        x = (double)i / 50.0;      // scale x
        double y = te_eval(expr); // evaluate expression

        int screen_x = i + WIDTH / 2;
        int screen_y = HEIGHT / 2 - (int)(y * 50.0);

        if (screen_y >= 0 && screen_y < HEIGHT) {
            SDL_Rect pixel = {screen_x - THICKNESS / 2, screen_y - THICKNESS / 2, THICKNESS, THICKNESS};
            SDL_FillRect(
                surface,
                &pixel,
                SDL_MapRGB(surface->format,
                           func_color.r,
                           func_color.g,
                           func_color.b)
            );
        }
    }

    te_free(expr);
}


int main(int argc, char* argv[])
{
    if (argc != 2) {
        printf("Usage: %s <expression>\n", argv[0]);
        return 0;
    }

    char *expr = argv[1];

    if (SDL_Init(SDL_INIT_VIDEO) != 0) {
        printf("SDL_Init Error: %s\n", SDL_GetError());
        return 1;
    }

    SDL_Window *win = SDL_CreateWindow("Function Plotter", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, WIDTH, HEIGHT, SDL_WINDOW_SHOWN);
    if (win == NULL) {
        printf("SDL_CreateWindow Error: %s\n", SDL_GetError());
        SDL_Quit();
        return 1;
    }

    SDL_Surface *surface = SDL_GetWindowSurface(win);
    SDL_FillRect(surface, NULL, SDL_MapRGB(surface->format, 255, 255, 255));

    draw_grid(surface);
    draw_axes(surface);
    draw_expression(surface, expr);
    SDL_UpdateWindowSurface(win);

    SDL_Event event;
    int app_running = 1;
    while(app_running){
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                app_running = 0;
            }
        }
    }
    SDL_DestroyWindow(win);
    SDL_Quit();
    return 0;
}