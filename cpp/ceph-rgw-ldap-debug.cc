#include <iostream>
#include <string.h>
#include <lber.h>
#include <ldap.h>
#include <errno.h>

#define nullptr NULL

using namespace std;

int main()
{
    LDAP *ldap;
    string binddn = "cn=Manager,dc=test,dc=com";
    string bindpw = "ustack";
    string searchdn = "ou=people,dc=test,dc=com";
    string searchfilter = "(uid=UID)";
    string dnattr = "uid";
    string pwd = "PASSWD";

    string uri = "ldap://HOST:PORT";

    int ret;
    ret = ldap_initialize(&ldap, uri.c_str());
    if (ret == LDAP_SUCCESS) {
        unsigned long ldap_ver = LDAP_VERSION3;
        ret = ldap_set_option(ldap, LDAP_OPT_PROTOCOL_VERSION,
                (void*) &ldap_ver);
    }
    if (ret == LDAP_SUCCESS) {
        ret = ldap_set_option(ldap, LDAP_OPT_REFERRALS, LDAP_OPT_OFF);
    }

    ret = ldap_simple_bind_s(ldap, binddn.c_str(), bindpw.c_str());
    char *attrs[] = { const_cast<char*>(dnattr.c_str()), nullptr };
    LDAPMessage *answer = nullptr, *entry = nullptr;

    ret = ldap_search_s(ldap, searchdn.c_str(), LDAP_SCOPE_SUBTREE,
            searchfilter.c_str(), attrs, 0, &answer);

    if (ret == LDAP_SUCCESS) {
        entry = ldap_first_entry(ldap, answer);
        if (entry) {
            char *dn = ldap_get_dn(ldap, entry);
            cout << dn << endl;
            LDAP* tldap;
            ret = ldap_initialize(&tldap, uri.c_str());
            if (ret == LDAP_SUCCESS) {
                unsigned long ldap_ver = LDAP_VERSION3;
                ret = ldap_set_option(tldap, LDAP_OPT_PROTOCOL_VERSION,
                        (void*) &ldap_ver);
                //ret = ldap_set_option(tldap, LDAP_OPT_REFERRALS, LDAP_OPT_OFF);
                if (ret == LDAP_SUCCESS) {
                    ret = ldap_simple_bind_s(tldap, dn, pwd.c_str());
                    cout << ldap_err2string(ret) << endl;
                    cout << ret << endl;
                    if (ret == LDAP_SUCCESS) {
                        (void) ldap_unbind(tldap);
                    }
                }
            }

            ldap_memfree(dn);
        }
    }
    ldap_msgfree(answer);

    return 0;
}
