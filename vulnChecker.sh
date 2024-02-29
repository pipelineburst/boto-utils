#!/bin/bash
for img in `echo $1 | sed 's/,/ /g'`; do
    echo $img | sed '/ /!s/^/eaa /' | tr '/:@' ' ' | while read -a image; do
    PRODUCT="$([ "${image[0]}" = "eaa" ] && echo "" || echo "${image[0]} ")"
    IMG="${image[3]} ${image[4]}";
    aws ecr describe-image-scan-findings --repository-name "${image[2]}/${image[3]}" --image-id "imageTag=${image[4]}" > out.txt 2>&1;
    if [ $? -ne 0 ]; then
       echo "$PRODUCT$IMG SUMMARY N/A N/A N/A N/A `egrep "An error occurred|Unable to" out.txt | cut -d" " -f1-4`"
       continue
    fi

    IMAGE_STATUS=$(jq -r '.imageScanStatus.status' out.txt);
    IMAGE_DATE=$(jq -r '.imageScanFindings.imageScanCompletedAt' out.txt);
    FORMATTED_IMAGE_DATE=$(echo "$IMAGE_DATE" | sed 's/T/ /; s/\..*//');

    aws inspector2 list-findings --no-cli-pager --cli-input-json "{\"filterCriteria\": {\"ecrImageRepositoryName\": [{\"comparison\": \"EQUALS\",\"value\": \"${image[2]}/${image[3]}\"}],\"ecrImageTags\": [{\"comparison\":\"EQUALS\", \"value\": \"${image[4]}\"}]}}" > out.txt;

    OUT=$(IMG="$PRODUCT$IMG" IMAGE_STATUS="$IMAGE_STATUS" jq -r '(.imageScanStatus.status),(.findings[]?|select(.status == "ACTIVE")|env.IMG+" "+.severity+" "+(.packageVulnerabilityDetails | "\(.vulnerablePackages[]|.name+":"+.version+" "+.filePath+" "+.fixedInVersion) \(.vulnerabilityId)"))' out.txt | grep -v UNTRIAGED | sed 's/LOW/MINOR/g' | sort | sed 's/MINOR/LOW/g' | grep -v 'null');
    echo "$OUT" >> vuln.txt;
    echo -n "$PRODUCT$IMG SUMMARY " >> vuln-symmary.txt;
    for SEV in CRITICAL HIGH MEDIUM LOW; do
        echo "$OUT" | grep $SEV | cut -d" " -f4,5 | sort | uniq | wc -l | tr '\n' ' ' >> vuln-symmary.txt;
    done;
    echo "$IMAGE_STATUS $FORMATTED_IMAGE_DATE" | tr '\n' ' ' >> vuln-symmary.txt;
    echo >> vuln-symmary.txt;
done
done