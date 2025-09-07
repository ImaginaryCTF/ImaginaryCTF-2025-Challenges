#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define MAX_CITY_LEN 32

// List of destinations
const char *cities[] = {
    "ROME",
    "MILAN",
    "VENICE",
    "FLORENCE",
    "NAPLES",
    "TURIN",
    "BOLOGNA",
    "GENOA",
    "PALERMO",
    "RIOMAGGIORE",
    "ANZIO",
    "PRATO",
    "RAGUSA",
    "FERRARA",
    "PISA"
};

const int city_count = sizeof(cities) / sizeof(cities[0]);
char current_airport[] = "ROME";

char selected_city[MAX_CITY_LEN] = {0};

void clear_booking() {
    for (int i = 0; i < city_count; i++) {
        unsetenv(cities[i]);
    }
}

const char *get_selected_city() {
    for (int i = 0; i < city_count; i++) {
        if (getenv(cities[i]) != NULL) {
            return cities[i];
        }
    }
    return NULL;
}

void feedback() {
    char feedback[256];
    puts("Enter your crash report here:");
    fgets(feedback, 256, stdin);
    puts("Sending your message to upper management:");
    printf(feedback);
}

void print_menu() {
    printf("--- Flight Booking System ---\n");
    printf("Current Airport: %s\n", current_airport);
    printf("Available Destinations:\n");

    for (int i = 0; i < city_count; i++) {
        printf("  %d) %s", i + 1, cities[i]);
        if (strcmp(selected_city, cities[i]) == 0) {
            printf("  [SELECTED]");
        }
        printf("\n");
    }

    printf("\nOptions:\n");
    printf("  s <num> - select destination\n");
    printf("  book    - confirm booking\n");
    printf("  exit    - quit program\n");
    printf("-----------------------------\n");
    printf("Choice: ");
}

int main() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);

    char *input = malloc(14);
    int blown = 0;

    while (1) {
        print_menu();
        if (!fgets(input, 14, stdin))
            break;

        // remove newline
        input[strcspn(input, "\n")] = 0;

	if (strncmp(input, "s ", 2) == 0) {
	    int choice = atoi(input + 2);

	    if (choice == 0) {
	        if (blown) {
	            puts("You still haven't figured out how to use this app?");
	            _exit(0);
	        }
	        printf("Error: Invalid airport number ");
                printf(input + 2);
                puts("");
	        blown = 1;
	    } else if (choice >= 1 && choice <= city_count) {
	        if (strcasecmp(cities[choice - 1], current_airport) == 0) {
	            printf("Error: Cannot select %s (already current airport).\n", current_airport);
	            clear_booking(); // reset any env vars
	        } else {
	            clear_booking();
	            if (setenv(cities[choice - 1], "1", 1) == 0) {
	                printf("Selected destination: %s\n", cities[choice - 1]);
	            } else {
	                perror("setenv");
	            }
	        }
	    } else {
	        printf("Invalid selection.\n");
	    }
        } else if (strcmp(input, "book") == 0) {
            const char *env_city = get_selected_city();
            if (env_city == NULL) {
                printf("No city selected.\n");
            } else if (strcasecmp(env_city, current_airport) == 0) {
                printf("Error: invalid flight\n");
                feedback();
                clear_booking();
            } else {
                printf("Successfully booked flight to %s!\n", env_city);
            }
        } else if (strcmp(input, "exit") == 0) {
            break;
        } else {
            printf("Unknown command.\n");
        }
    }

    _exit(0);
}
