import curses
import time
import random

def main(stdscr):
    # Initialize curses
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    sh, sw = stdscr.getmaxyx()

    # Create the player
    player = '^'
    player_x = sw // 2
    player_y = sh - 1

    # Create the bullets
    bullets = []

    # Create the enemies
    enemies = []
    level = 1  # Initialize level
    max_levels = 3  # Set the maximum number of levels

    def reset_level():
        nonlocal player_x, player_y, bullets, enemies, level
        player_x = sw // 2
        player_y = sh - 1
        bullets = []
        enemies = []
        for _ in range(5 + level * 2):
            enemy_x = random.randint(1, sw - 2)
            enemy_y = random.randint(1, sh - 2)
            enemies.append([enemy_y, enemy_x])

    while True:
        # Get user input
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == ord(' '):  # Spacebar
            bullets.append([player_y - 1, player_x])
        elif key == curses.KEY_RIGHT and player_x < sw - 1:
            player_x += 1
        elif key == curses.KEY_LEFT and player_x > 0:
            player_x -= 1

        # Move bullets
        new_bullets = []
        for bullet in bullets:
            if bullet[0] > 0:
                new_bullets.append([bullet[0] - 1, bullet[1]])
        bullets = new_bullets

        # Move enemies
        new_enemies = []
        for enemy in enemies:
            if enemy[0] < sh - 1:
                new_enemies.append([enemy[0] + 1, enemy[1]])
            else:
                # Respawn enemies at the top
                new_enemies.append([0, random.randint(1, sw - 2)])
        enemies = new_enemies

        # Check for collisions
        for bullet in bullets:
            if bullet in enemies:
                enemies.remove(bullet)
                bullets.remove(bullet)

        # Draw everything
        stdscr.clear()
        stdscr.addch(player_y, player_x, player)
        for bullet in bullets:
            stdscr.addch(bullet[0], bullet[1], '*')
        for enemy in enemies:
            stdscr.addch(enemy[0], enemy[1], 'E')
        stdscr.addstr(0, 2, f'Level: {level}')
        stdscr.refresh()

        # Game over condition
        if [player_y, player_x] in enemies:
            stdscr.addstr(sh // 2, sw // 2 - 10, f'Game Over - Your Score: {level}', curses.A_BOLD)
            stdscr.addstr(sh // 2 + 1, sw // 2 - 15, 'Press q to quit', curses.A_BOLD)
            stdscr.refresh()
            while True:
                key = stdscr.getch()
                if key == ord('q'):
                    break
            break

        # Check if all enemies are cleared for the current level
        if not enemies:
            level += 1
            if level > max_levels:
                stdscr.addstr(sh // 2, sw // 2 - 10, 'You Win!', curses.A_BOLD)
                stdscr.addstr(sh // 2 + 1, sw // 2 - 15, 'Press q to quit', curses.A_BOLD)
                stdscr.refresh()
                while True:
                    key = stdscr.getch()
                    if key == ord('q'):
                        break
                break
            else:
                reset_level()
                stdscr.addstr(sh // 2, sw // 2 - 5, f'Level {level}', curses.A_BOLD)
                stdscr.refresh()
                time.sleep(2)

curses.wrapper(main)
