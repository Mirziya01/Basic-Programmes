#include "raylib.h"
#include <time.h>
#include <math.h>

#define WIDTH 800
#define HEIGHT 600

#define NUM_PARTICLES 50

typedef struct Particle {
    Vector2 position;
    Vector2 velocity;
    float radius;
    Color color;
} Particle;

Particle particles[NUM_PARTICLES];

void ParticleCollision(Particle *p1, Particle *p2)
{
    float dx = p2->position.x - p1->position.x;
    float dy = p2->position.y - p1->position.y;
    float distance = sqrtf(dx * dx + dy * dy);

    if (distance < p1->radius + p2->radius)
    {
        // Simple elastic collision response
        float angle = atan2f(dy, dx);
        float targetX = p1->position.x + cosf(angle) * (p1->radius + p2->radius);
        float targetY = p1->position.y + sinf(angle) * (p1->radius + p2->radius);
        float ax = (targetX - p2->position.x) * 0.5f;
        float ay = (targetY - p2->position.y) * 0.5f;

        p1->velocity.x -= ax;
        p1->velocity.y -= ay;
        p2->velocity.x += ax;
        p2->velocity.y += ay;
    }
}

void UpdateParticle(Particle *p)
{
    p->position.x += p->velocity.x;
    p->position.y += p->velocity.y;

    // Check for collision with window borders
    if ((p->position.x - p->radius < 0) || (p->position.x + p->radius > WIDTH))
    {
        p->velocity.x *= -1; // Reverse X velocity
    }
    if ((p->position.y - p->radius < 0) || (p->position.y + p->radius > HEIGHT))
    {
        p->velocity.y *= -1; // Reverse Y velocity
    }

    // Check for collision with other particles
    Particle *other;
    for (int i = 0; i < NUM_PARTICLES; i++)
    {
        other = &particles[i];
        if (other != p)
        {
            ParticleCollision(p, other);
        }
    }
}

void DrawParticle(Particle *p)
{
    DrawCircleV(p->position, p->radius, p->color);
}

void UpdateParticles(void)
{
    for (int i = 0; i < NUM_PARTICLES; i++)
    {
        UpdateParticle(&particles[i]);
    }
}

void DrawParticles(void)
{
    for (int i = 0; i < NUM_PARTICLES; i++)
    {
        DrawParticle(&particles[i]);
    }
}

void InitParticles(void)
{
    SetRandomSeed((unsigned int)time(NULL));
    for (int i = 0; i < NUM_PARTICLES; i++)
    {
        float r = (float)GetRandomValue(5, 15);
        particles[i].radius = r;
        particles[i].position = (Vector2){ GetRandomValue(r, WIDTH - r), GetRandomValue(r, HEIGHT - r) };
        particles[i].velocity = (Vector2){ GetRandomValue(-3, 3), GetRandomValue(-3, 3) };
        particles[i].color = (Color){ GetRandomValue(50, 255), GetRandomValue(50, 255), GetRandomValue(50, 255), 255 };
    }
}

int main(void)
{
    InitWindow(WIDTH, HEIGHT, "Particle Collision Simulation");

    InitParticles();
    SetTargetFPS(60);
    while (!WindowShouldClose())
    {
        BeginDrawing();
            ClearBackground(BLACK);
            // Particle simulation and rendering logic would go here
            UpdateParticles();
            DrawParticles();
            DrawFPS(5, 5);
        EndDrawing();
    }

    CloseWindow();

    return 0;
}