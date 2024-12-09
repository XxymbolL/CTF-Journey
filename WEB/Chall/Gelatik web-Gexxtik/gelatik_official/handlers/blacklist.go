package handlers

import (
	"fmt"
	"net"
	"net/url"
	"strings"
)

type BlacklistChecker struct {
	blacklistedPatterns []string
	blacklistedCIDRs    []*net.IPNet
}

func NewBlacklistChecker() *BlacklistChecker {
	checker := &BlacklistChecker{
		blacklistedPatterns: []string{
			"localhost",
		},
	}

	// Add CIDR ranges
	cidrs := []string{
		"127.0.0.0/8", // IPv4 localhost
		"172.0.0.0/8", // IPv4 private
		"192.0.0.0/8", // IPv4 private
		"::1/128",     // IPv6 localhost
		"0.0.0.0/8",   // IPv4 broadcast
		"fe80::/10",   // IPv6 link-local
	}

	for _, cidr := range cidrs {
		_, network, err := net.ParseCIDR(cidr)
		if err == nil {
			checker.blacklistedCIDRs = append(checker.blacklistedCIDRs, network)
		}
	}

	return checker
}

func (b *BlacklistChecker) isIPBlacklisted(ipStr string) bool {
	ip := net.ParseIP(ipStr)
	if ip == nil {
		return false
	}

	for _, network := range b.blacklistedCIDRs {
		if network.Contains(ip) {
			return true
		}
	}

	return false
}

func (b *BlacklistChecker) IsBlacklisted(urlStr string) (bool, error) {
	parsedURL, err := url.Parse(urlStr)
	if err != nil {
		return false, fmt.Errorf("error parsing URL: %v", err)
	}

	host := strings.ToLower(parsedURL.Hostname())

	// Check patterns
	for _, pattern := range b.blacklistedPatterns {
		if strings.Contains(host, pattern) {
			return true, nil
		}
	}

	// Check if hostname is an IP address
	if ip := net.ParseIP(host); ip != nil {
		if b.isIPBlacklisted(host) {
			return true, nil
		}
	} else {
		// If hostname is not an IP, resolve it
		ips, err := net.LookupIP(host)
		if err != nil {
			return false, fmt.Errorf("error resolving hostname %s: %v", host, err)
		}

		for _, ip := range ips {
			if b.isIPBlacklisted(ip.String()) {
				return true, nil
			}
		}
	}

	return false, nil
}
