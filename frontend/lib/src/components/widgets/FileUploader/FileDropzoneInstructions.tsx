/**
 * Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022-2026)
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import { memo } from "react"

import { CloudUpload } from "@emotion-icons/material-outlined"

import Icon from "~lib/components/shared/Icon"
import { FileSize, getSizeDisplay } from "~lib/util/FileHelper"

import {
  StyledFileDropzoneInstructions,
  StyledFileDropzoneInstructionsColumn,
  StyledFileDropzoneInstructionsFileUploaderIcon,
  StyledFileDropzoneInstructionsSubtext,
  StyledFileDropzoneInstructionsText,
} from "./styled-components"

export interface Props {
  multiple: boolean
  acceptedExtensions: string[]
  maxSizeBytes: number
  acceptDirectory?: boolean
  disabled?: boolean
}

const FileDropzoneInstructions = ({
  multiple,
  acceptedExtensions,
  maxSizeBytes,
  acceptDirectory = false,
  disabled,
}: Props): React.ReactElement => {
  // Determine what type of content we're accepting
  const getContentTypeText = (): string => {
    if (acceptDirectory) {
      return "directories"
    }
    return multiple ? "files" : "file"
  }

  const getFileTypeInfo = (): string | null => {
    if (acceptedExtensions.length) {
      // Remove duplicate display of JPG/JPEG - show only JPG
      const deduplicatedExtensions = acceptedExtensions
        .map(ext => ext.replace(/^\./, "").toUpperCase())
        .filter((ext, index, arr) => {
          // If this is JPEG and JPG is also present, filter out JPEG
          if (ext === "JPEG" && arr.includes("JPG")) {
            return false
          }
          return true
        })

      return ` • ${deduplicatedExtensions.join(", ")}`
    }
    return null
  }

  const getSizeLimit = (): string => {
    return `Limit ${getSizeDisplay(maxSizeBytes, FileSize.Byte, 0)} per file`
  }

  return (
    <StyledFileDropzoneInstructions data-testid="stFileUploaderDropzoneInstructions">
      <StyledFileDropzoneInstructionsFileUploaderIcon>
        <Icon content={CloudUpload} size="threeXL" />
      </StyledFileDropzoneInstructionsFileUploaderIcon>
      <StyledFileDropzoneInstructionsColumn>
        <StyledFileDropzoneInstructionsText disabled={disabled}>
          Drag and drop {getContentTypeText()} here
        </StyledFileDropzoneInstructionsText>
        <StyledFileDropzoneInstructionsSubtext disabled={disabled}>
          {getSizeLimit()}
          {getFileTypeInfo()}
        </StyledFileDropzoneInstructionsSubtext>
      </StyledFileDropzoneInstructionsColumn>
    </StyledFileDropzoneInstructions>
  )
}

export default memo(FileDropzoneInstructions)
